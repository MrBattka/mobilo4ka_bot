#!/usr/bin/env python3
"""Daily product scraper for trubkoved.ru.

Exports product name, URL, and price to CSV and JSON.
Uses only Python standard library so it can run from cron without installs.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape as xml_escape
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE_URL = "https://trubkoved.ru"
CATALOG_URL = f"{BASE_URL}/catalog/"
DEFAULT_OUTPUT_DIR = Path("outputs")
DESKTOP_XLSX_PATH = Path.home() / "Desktop" / "Парсер Трубковед Стор77.xlsx"
DEFAULT_SECTION_PATHS = (
    "/catalog/smartfony/",
    "/catalog/planshety/",
    "/catalog/noutbuki/",
    "/catalog/umnye-chasy/",
)
USER_AGENT = (
    "Mozilla/5.0 (compatible; TrubkovedProductScraper/1.0; "
    "+https://trubkoved.ru)"
)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}
MAX_PAGES = int(os.environ.get("TRUBKOVED_MAX_PAGES", "0"))
EMPTY_PAGE_LIMIT = int(os.environ.get("TRUBKOVED_EMPTY_PAGE_LIMIT", "6"))

@dataclass(frozen=True)
class Product:
    name: str
    url: str
    price: str
    price_value: int | None
    source_url: str
    scraped_at: str


def fetch(url: str, timeout: int = 25, retries: int = 3) -> str:
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            request = Request(url, headers=DEFAULT_HEADERS)
            with urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Could not fetch {url}: {last_error}")


def clean_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()
    return value


def absolute_url(href: str) -> str:
    return urljoin(BASE_URL, html.unescape(href))


def available_url(section_url: str, page: int = 1) -> str:
    if page <= 1:
        return f"{section_url}?only_available=Y"
    return f"{section_url}?only_available=Y&PAGEN_1={page}"


def price_number(price: str) -> int | None:
    digits = re.sub(r"\D+", "", price)
    return int(digits) if digits else None


def discover_catalog_sections(catalog_html: str) -> list[str]:
    hrefs = set()
    for href in re.findall(r'href=["\']([^"\']+)["\']', catalog_html):
        parsed = urlparse(absolute_url(href))
        if parsed.netloc != urlparse(BASE_URL).netloc:
            continue
        path = parsed.path
        if not path.startswith("/catalog/"):
            continue
        if path in {"/catalog/", "/catalog/compare.php"}:
            continue
        if not path.endswith("/"):
            continue
        hrefs.add(urljoin(BASE_URL, path))
    return sorted(hrefs)


def discover_pages(section_url: str, section_html: str) -> list[str]:
    page_numbers = {1}
    for href in re.findall(r'href=["\']([^"\']*PAGEN_1=\d+[^"\']*)["\']', section_html):
        page_numbers.add(page_number(absolute_url(href)))

    max_page = max(page_numbers)
    pages = [available_url(section_url)]
    pages.extend(available_url(section_url, number) for number in range(2, max_page + 1))
    return pages


def page_number(url: str) -> int:
    match = re.search(r"[?&]PAGEN_1=(\d+)", url)
    return int(match.group(1)) if match else 1


def product_blocks(page_html: str) -> Iterable[str]:
    pattern = re.compile(
        r'<div class="catalog-block__wrapper\b.*?(?=<div class="catalog-block__wrapper\b|<div class="bottom_nav\b|$)',
        re.DOTALL,
    )
    yield from (match.group(0) for match in pattern.finditer(page_html))


def parse_data_item(block: str) -> dict[str, object]:
    match = re.search(r'data-item=(["\'])(.*?)\1', block, re.DOTALL)
    if not match:
        return {}
    raw = html.unescape(match.group(2))
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def parse_product(block: str, source_url: str, scraped_at: str) -> Product | None:
    has_cart_button = bool(
        re.search(
            r'<button[^>]+class="[^"]*\bto_cart\b[^"]*"[^>]+data-action=["\']basket["\'][^>]*>',
            block,
            re.DOTALL,
        )
    )
    if not has_cart_button:
        return None

    data_item = parse_data_item(block)

    name = clean_text(str(data_item.get("NAME") or ""))
    href = str(data_item.get("DETAIL_PAGE_URL") or "").strip()

    if not name or not href:
        title_match = re.search(
            r'<div class="catalog-block__info-title.*?<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            block,
            re.DOTALL,
        )
        if title_match:
            href = href or title_match.group(1)
            name = name or clean_text(title_match.group(2))

    price_match = re.search(
        r'<span class="price__new-val[^"]*">(.*?)</span>',
        block,
        re.DOTALL,
    )
    price = clean_text(price_match.group(1)) if price_match else ""

    if not name or not href or not price:
        return None

    return Product(
        name=name,
        url=absolute_url(href),
        price=price,
        price_value=price_number(price),
        source_url=source_url,
        scraped_at=scraped_at,
    )


def goto_with_retry(page, url: str) -> None:
    for attempt in range(1, 4):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            page.wait_for_timeout(1_500)
            return
        except PlaywrightTimeoutError:
            if page.locator("div.catalog-block__wrapper").count() > 0:
                return
            if attempt == 3:
                raise
            print(f"  retry {attempt}/3: {url}", file=sys.stderr)
            page.wait_for_timeout(3_000 * attempt)


def discover_browser_pages(page, section_url: str) -> list[str]:
    goto_with_retry(page, available_url(section_url))

    numbers = {1}
    links = page.locator('a[href*="PAGEN_1="]').all()

    for link in links:
        href = link.get_attribute("href") or ""
        match = re.search(r"[?&]PAGEN_1=(\d+)", href)
        if match:
            numbers.add(int(match.group(1)))

    last_page = max(numbers)

    if MAX_PAGES > 0:
        last_page = min(last_page, MAX_PAGES)

    return [
        available_url(section_url, page_number)
        for page_number in range(1, last_page + 1)
    ]


def scrape_browser_page(
    page,
    url: str,
    scraped_at: str,
) -> list[Product]:
    goto_with_retry(page, url)

    products = []

    for block in page.locator("div.catalog-block__wrapper").all():
        try:
            block_html = block.evaluate(
                "(element) => element.outerHTML"
            )
            product = parse_product(block_html, page.url, scraped_at)

            if product:
                products.append(product)

        except Exception as exc:
            print(f"  product parse failed: {exc}", file=sys.stderr)

    return products

def scrape(
    max_sections: int | None = None,
    delay: float = 0.5,
    section_paths: tuple[str, ...] = DEFAULT_SECTION_PATHS,
) -> list[Product]:
    scraped_at = datetime.now().astimezone().isoformat(timespec="seconds")

    section_urls = [
        urljoin(BASE_URL, path)
        for path in section_paths
    ]

    if max_sections is not None:
        section_urls = section_urls[:max_sections]

    products_by_url: dict[str, Product] = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=DEFAULT_HEADERS["User-Agent"],
            locale="ru-RU",
        )
        page.set_default_timeout(20_000)

        try:
            for section_index, section_url in enumerate(
                section_urls,
                start=1,
            ):
                print(
                    f"[trubkoved {section_index}/{len(section_urls)}] "
                    f"{section_url}",
                    file=sys.stderr,
                )

                try:
                    pages = discover_browser_pages(page, section_url)
                except Exception as exc:
                    print(
                        f"  section failed: {exc}",
                        file=sys.stderr,
                    )
                    continue

                empty_streak = 0

                for page_index, current_url in enumerate(
                    pages,
                    start=1,
                ):
                    before = len(products_by_url)

                    try:
                        products = scrape_browser_page(
                            page,
                            current_url,
                            scraped_at,
                        )

                        for product in products:
                            products_by_url[product.url] = product

                    except Exception as exc:
                        print(
                            f"  page failed: {current_url} -> {exc}",
                            file=sys.stderr,
                        )

                    added = len(products_by_url) - before

                    print(
                        f"  page {page_index}/{len(pages)}: +{added}",
                        file=sys.stderr,
                    )

                    empty_streak = (
                        empty_streak + 1
                        if added == 0
                        else 0
                    )

                    if (
                        EMPTY_PAGE_LIMIT > 0
                        and empty_streak >= EMPTY_PAGE_LIMIT
                    ):
                        print(
                            f"  stop section after {empty_streak} "
                            f"empty pages",
                            file=sys.stderr,
                        )
                        break

                    time.sleep(delay)

        finally:
            browser.close()

    products = sorted(
        products_by_url.values(),
        key=lambda product: product.url,
    )

    print(
        f"Done trubkoved: {len(products)} unique products",
        file=sys.stderr,
    )

    return products


def excel_column(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def inline_string_cell(row: int, col: int, value: str, style: int = 0) -> str:
    ref = f"{excel_column(col)}{row}"
    style_attr = f' s="{style}"' if style else ""
    escaped = xml_escape(value)
    return f'<c r="{ref}" t="inlineStr"{style_attr}><is><t>{escaped}</t></is></c>'


def number_cell(row: int, col: int, value: int | float, style: int = 0) -> str:
    ref = f"{excel_column(col)}{row}"
    style_attr = f' s="{style}"' if style else ""
    return f'<c r="{ref}"{style_attr}><v>{value}</v></c>'


def write_xlsx(products: list[Product], xlsx_path: Path) -> None:
    try:
        import xlsxwriter
    except ImportError:
        xlsxwriter = None

    if xlsxwriter is not None:
        workbook = xlsxwriter.Workbook(xlsx_path)
        worksheet = workbook.add_worksheet("Товары")
        header_format = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#EAF3F8",
                "bottom": 1,
                "bottom_color": "#A6A6A6",
            }
        )
        price_format = workbook.add_format({"num_format": "0"})

        worksheet.write_row(0, 0, ["Название", "Цена", "Ссылка"], header_format)
        for row_index, product in enumerate(products, start=1):
            price = product.price_value if product.price_value is not None else 0
            worksheet.write(row_index, 0, product.name)
            worksheet.write_number(row_index, 1, price, price_format)
            worksheet.write(row_index, 2, product.url)

        worksheet.set_column(0, 0, 58)
        worksheet.set_column(1, 1, 14)
        worksheet.set_column(2, 2, 82)
        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(0, 0, len(products), 2)
        workbook.close()
        return

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    rows = [
        '<row r="1">'
        + inline_string_cell(1, 1, "Название", 1)
        + inline_string_cell(1, 2, "Цена", 1)
        + inline_string_cell(1, 3, "Ссылка", 1)
        + "</row>"
    ]

    for row_index, product in enumerate(products, start=2):
        price = product.price_value if product.price_value is not None else 0
        rows.append(
            f'<row r="{row_index}">'
            + inline_string_cell(row_index, 1, product.name)
            + number_cell(row_index, 2, price, 2)
            + inline_string_cell(row_index, 3, product.url)
            + "</row>"
        )

    last_row = len(products) + 1
    sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetViews>
    <sheetView workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft" activeCell="A2" sqref="A2"/>
    </sheetView>
  </sheetViews>
  <cols>
    <col min="1" max="1" width="58" customWidth="1"/>
    <col min="2" max="2" width="14" customWidth="1"/>
    <col min="3" max="3" width="82" customWidth="1"/>
  </cols>
  <sheetData>
    {''.join(rows)}
  </sheetData>
  <autoFilter ref="A1:C{last_row}"/>
</worksheet>'''

    workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Товары" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFEAF3F8"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left/><right/><top/><bottom style="thin"><color rgb="FFA6A6A6"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="1" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''

    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    app_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Python</Application>
</Properties>'''

    core_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:creator>Trubkoved parser</dc:creator>
  <cp:lastModifiedBy>Trubkoved parser</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''

    with zipfile.ZipFile(xlsx_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("docProps/app.xml", app_xml)
        archive.writestr("docProps/core.xml", core_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/styles.xml", styles_xml)
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def write_outputs(products: list[Product], output_dir: Path) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    csv_path = output_dir / f"trubkoved_products_{stamp}.csv"
    json_path = output_dir / f"trubkoved_products_{stamp}.json"
    xlsx_path = output_dir / f"trubkoved_products_{stamp}.xlsx"

    fields = ["name", "price", "url"]
    csv_rows = [
        {
            "name": product.name,
            "price": product.price_value if product.price_value is not None else "",
            "url": product.url,
        }
        for product in products
    ]
    json_rows = [product.__dict__ for product in products]

    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(csv_rows)

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(json_rows, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    write_xlsx(products, xlsx_path)

    (output_dir / "trubkoved_products_latest.csv").write_bytes(csv_path.read_bytes())
    (output_dir / "trubkoved_products_latest.json").write_bytes(json_path.read_bytes())
    (output_dir / "trubkoved_products_latest.xlsx").write_bytes(xlsx_path.read_bytes())
    if os.environ.get("TRUBKOVED_SKIP_DESKTOP") != "1":
        DESKTOP_XLSX_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            DESKTOP_XLSX_PATH.write_bytes(xlsx_path.read_bytes())
        except OSError as exc:
            print(f"Warning: could not save desktop copy to {DESKTOP_XLSX_PATH}: {exc}", file=sys.stderr)
    return csv_path, json_path, xlsx_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape trubkoved.ru products.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-sections", type=int, default=None, help="Debug limit.")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between page requests.")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Ограничение количества страниц раздела.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    products: list[Product] = []

    if args.max_pages is not None:
        os.environ["TRUBKOVED_MAX_PAGES"] = str(args.max_pages)
        
    try:
        products = scrape(max_sections=args.max_sections, delay=args.delay)
    except Exception as exc:
        print(f"Trubkoved parse failed: {exc}", file=sys.stderr)
        # не обнуляем результат, если уже были собраны данные
        products = []

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path, json_path, xlsx_path = write_outputs(products, output_dir)

    print(csv_path)
    print(json_path)
    print(xlsx_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
