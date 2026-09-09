#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import csv
from datetime import datetime
from pathlib import Path

from scrape_trubkoved import Product, write_xlsx


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
SOURCE_FILES = [
    OUTPUT_DIR / "trubkoved_products_latest.json",
    OUTPUT_DIR / "store77_products_latest.json",
    OUTPUT_DIR / "boltyn_products_latest.json",
]


def load_products(path: Path) -> list[Product]:
    if not path.exists():
        return []
    rows = json.loads(path.read_text("utf-8"))
    products = []
    for item in rows:
        products.append(
            Product(
                name=item["name"],
                url=item["url"],
                price=str(item.get("price") or item.get("price_value") or ""),
                price_value=item.get("price_value"),
                source_url=item.get("source_url", item["url"]),
                scraped_at=item.get("scraped_at", ""),
            )
        )
    return products


def main() -> int:
    products_by_url: dict[str, Product] = {}
    for source_file in SOURCE_FILES:
        for product in load_products(source_file):
            products_by_url[product.url] = product

    products = sorted(products_by_url.values(), key=lambda item: item.url)
    stamp = datetime.now().strftime("%Y-%m-%d")
    csv_path = OUTPUT_DIR / f"products_{stamp}.csv"
    json_path = OUTPUT_DIR / f"products_{stamp}.json"
    xlsx_path = OUTPUT_DIR / f"products_{stamp}.xlsx"

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
        writer = csv.DictWriter(handle, fieldnames=["name", "price", "url"], delimiter=";")
        writer.writeheader()
        writer.writerows(csv_rows)

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(json_rows, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    write_xlsx(products, xlsx_path)

    shutil.copy2(csv_path, OUTPUT_DIR / "products_latest.csv")
    shutil.copy2(json_path, OUTPUT_DIR / "products_latest.json")
    shutil.copy2(xlsx_path, OUTPUT_DIR / "products_latest.xlsx")
    desktop_xlsx = Path.home() / "Desktop" / "Парсер Трубковед Стор77.xlsx"
    try:
        shutil.copy2(OUTPUT_DIR / "products_latest.xlsx", desktop_xlsx)
    except OSError as exc:
        print(f"Warning: could not save desktop copy to {desktop_xlsx}: {exc}")
    print(f"combined={len(products)}")
    print(csv_path)
    print(json_path)
    print(xlsx_path)
    print(OUTPUT_DIR / "products_latest.xlsx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
