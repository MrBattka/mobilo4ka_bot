import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = path.join(ROOT, "outputs");
const BASE_URL = "https://applegod.ru";
const CONCURRENCY = 12;

const APPLEGOD_SECTIONS = [
  "https://applegod.ru/shop/apple/",
  "https://applegod.ru/shop/samsung/",
];

function todayStamp() {
  const now = new Date();

  return [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, "0"),
    String(now.getDate()).padStart(2, "0"),
  ].join("-");
}

function normalizeUrl(value) {
  try {
    const url = new URL(value, BASE_URL);
    url.hash = "";

    return url.href.replace(/\/+$/, "");
  } catch {
    return "";
  }
}

function pageUrl(sectionUrl, pageNumber) {
  const url = new URL(sectionUrl);

  if (pageNumber <= 1) {
    url.searchParams.delete("PAGEN_1");
  } else {
    url.searchParams.set("PAGEN_1", String(pageNumber));
  }

  return url.href;
}

async function configurePage(page) {
  await page.route("**/*", async (route) => {
    const resourceType = route.request().resourceType();

    if (["image", "media", "font"].includes(resourceType)) {
      await route.abort();
      return;
    }

    await route.continue();
  });
}

async function gotoWithRetry(page, url) {
  for (let attempt = 1; attempt <= 2; attempt += 1) {
    try {
      await page.goto(url, {
        waitUntil: "domcontentloaded",
        timeout: 15000,
      });
      return;
    } catch (error) {
      if (attempt === 2) throw error;
      await page.waitForTimeout(500);
    }
  }
}

async function discoverPages(page, sectionUrl) {
  await gotoWithRetry(page, sectionUrl);

  const maxPage = await page.evaluate(() => {
    const links = [...document.querySelectorAll(".bx-pagination a[href]")];
    const pages = links
      .map((link) => {
        try {
          return Number(new URL(link.href).searchParams.get("PAGEN_1"));
        } catch {
          return 0;
        }
      })
      .filter((n) => Number.isInteger(n) && n > 0);

    return pages.length ? Math.max(...pages) : 1;
  });

  return Array.from({ length: maxPage }, (_, i) => pageUrl(sectionUrl, i + 1));
}

async function scrapePage(page, url, scrapedAt) {
  await gotoWithRetry(page, url);

  return page.evaluate(({ scrapedAt }) => {
    const clean = (value) => String(value ?? "").replace(/\s+/g, " ").trim();

    const cards = [...document.querySelectorAll(
      '.products__col[data-entity="item"] .card-product'
    )];

    const seen = new Set();
    const result = [];

    for (const card of cards) {
      const name = clean(card.querySelector('.card-product__title a[itemprop="name"]')?.textContent);

      const linkNode = card.querySelector('.card-product__title a[href]');
      const href = linkNode?.href || "";
      const priceNode = card.querySelector('meta[itemprop="price"]') || card.querySelector('.card-product__price');

      if (!name || !href) continue;

      const priceText = priceNode?.getAttribute("content") || priceNode?.textContent || "0";
      const price = Number(String(priceText).replace(/\D/g, "")) || 0;

      if (!price || seen.has(href)) continue;

      seen.add(href);
      result.push({
        name,
        price: String(price),
        price_value: price,
        url: href,
        source: "applegod",
        scraped_at: scrapedAt,
      });
    }

    return result;
  }, { scrapedAt });
}

async function scrapePagesConcurrent(browser, pages, scrapedAt) {
  const results = [];
  let index = 0;

  const worker = async () => {
    while (index < pages.length) {
      const current = index++;
      const url = pages[current];

      const page = await browser.newPage({
        viewport: { width: 1280, height: 900 },
      });

      try {
        const products = await scrapePage(page, url, scrapedAt);
        results.push(...products);
      } catch (e) {
        console.error(`Skip ${url}: ${e.message || e}`);
      } finally {
        await page.close();
      }
    }
  };

  await Promise.all(
    Array.from({ length: Math.min(CONCURRENCY, pages.length) }, () => worker())
  );

  return results;
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  const scrapedAt = new Date().toISOString();

  const browser = await chromium.launch({
    headless: true,
  });

  const productsByUrl = new Map();

  try {
    for (
      const [sectionIndex, sectionUrl]
      of APPLEGOD_SECTIONS.entries()
    ) {
      console.error(
        `[applegod ${sectionIndex + 1}/${APPLEGOD_SECTIONS.length}] ${sectionUrl}`,
      );

      const discoveryPage = await browser.newPage({
        userAgent:
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
        viewport: { width: 1440, height: 900 },
      });

      try {
        await configurePage(discoveryPage);

        const pages = await discoverPages(
          discoveryPage,
          sectionUrl,
        );

        console.error(
          `  Found ${pages.length} pages to scrape.`,
        );

        const sectionProducts = await scrapePagesConcurrent(
          browser,
          pages,
          scrapedAt,
        );

        for (const product of sectionProducts) {
          const productUrl = normalizeUrl(product.url);

          if (productUrl) {
            productsByUrl.set(productUrl, {
              ...product,
              url: productUrl,
            });
          }
        }

        console.error(
          `  Section products collected: ${sectionProducts.length}`,
        );
      } finally {
        await discoveryPage.close();
      }
    }
  } finally {
    await browser.close();
  }

  const products = [...productsByUrl.values()].sort(
    (a, b) => a.url.localeCompare(b.url),
  );

  const datedPath = path.join(
    OUTPUT_DIR,
    `applegod_products_${todayStamp()}.json`,
  );

  const latestPath = path.join(
    OUTPUT_DIR,
    "applegod_products_latest.json",
  );

  const content = JSON.stringify(products, null, 2) + "\n";

  await fs.writeFile(datedPath, content, "utf8");
  await fs.writeFile(latestPath, content, "utf8");

  console.error(
    `Done applegod: ${products.length} unique products saved to ${latestPath}`,
  );
}

main().catch((error) => {
  console.error(error?.stack || error);
  process.exit(1);
});