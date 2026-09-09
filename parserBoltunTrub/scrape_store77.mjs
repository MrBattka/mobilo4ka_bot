import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = path.join(ROOT, "outputs");
const BASE_URL = "https://store77.net";

const STORE77_SECTIONS = [
  "https://store77.net/planshety_apple/",
  "https://store77.net/apple_macbook/",
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

function isNavigationError(error) {
  const message = String(error?.message || error);

  return (
    message.includes("Execution context was destroyed") ||
    message.includes("Target page, context or browser has been closed") ||
    message.includes("frame was detached")
  );
}

async function gotoWithRetry(page, url) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      await page.goto(url, {
        waitUntil: "domcontentloaded",
        timeout: 60000,
      });

      // Даём сайту завершить возможный redirect/динамическую загрузку.
      await page.waitForTimeout(1000);
      return;
    } catch (error) {
      if (attempt === 3) {
        throw error;
      }

      console.error(`  Navigation retry ${attempt}/3: ${url}`);
      await page.waitForTimeout(attempt * 3000);
    }
  }
}

async function evaluateWithRetry(page, callback, argument = undefined) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      return await page.evaluate(callback, argument);
    } catch (error) {
      if (!isNavigationError(error) || attempt === 3) {
        throw error;
      }

      await page.waitForTimeout(attempt * 1000);
    }
  }

  throw new Error("Unable to evaluate page content");
}

async function discoverPages(page, sectionUrl) {
  await gotoWithRetry(page, sectionUrl);

  const pageNumbers = await evaluateWithRetry(page, () => {
    const numbers = new Set([1]);

    for (const anchor of document.querySelectorAll("a[href]")) {
      try {
        const url = new URL(anchor.href);
        const pageNumber = url.searchParams.get("PAGEN_1");

        if (pageNumber && /^\d+$/.test(pageNumber)) {
          numbers.add(Number(pageNumber));
        }
      } catch {
        // Некорректные ссылки пропускаем.
      }
    }

    return [...numbers].filter(
      (number) => Number.isInteger(number) && number > 0,
    );
  });

  const maxPage = Math.max(1, ...pageNumbers);

  console.error(`  Pagination pages detected: ${maxPage}`);

  return Array.from(
    { length: maxPage },
    (_, index) => pageUrl(sectionUrl, index + 1),
  );
}

async function scrapePage(page, url, scrapedAt) {
  await gotoWithRetry(page, url);

  const products = await evaluateWithRetry(
    page,
    ({ scrapedAt }) => {
      function clean(value) {
        return String(value || "").replace(/\s+/g, " ").trim();
      }

      function parsePrice(value) {
        const text = String(value || "")
          .replace(/\u00a0/g, " ")
          .replace(/\s/g, "");

        const match = text.match(/\d+(?:[.,]\d+)?/);

        if (!match) {
          return 0;
        }

        const price = Number(match[0].replace(",", "."));
        return Number.isFinite(price) && price > 0 ? price : 0;
      }

      function absolute(value) {
        try {
          return new URL(value, location.origin).href;
        } catch {
          return "";
        }
      }

      const cards = [
        ...document.querySelectorAll(".blocks_product"),
      ];

      const result = [];
      const seen = new Set();

      for (const card of cards) {
        const buyButton = card.querySelector(
          ".card-product-buy-button-list[data-price]",
        );

        const priceElement = card.querySelector(
          "[data-price], .card-product-price, .price",
        );

        const price = parsePrice(
          buyButton?.getAttribute("data-price") ||
            priceElement?.textContent,
        );

        const link = card.querySelector(
          ".blocks_product_fix_w > a[href], a[href]",
        );

        const image = card.querySelector("img[title], img[alt]");

        const name = clean(
          image?.getAttribute("title") ||
            image?.getAttribute("alt") ||
            link?.getAttribute("title") ||
            link?.textContent,
        );

        const productUrl = absolute(link?.getAttribute("href") || "");

        if (!name || !productUrl || !price || seen.has(productUrl)) {
          continue;
        }

        seen.add(productUrl);

        result.push({
          name,
          url: productUrl,
          price: String(price),
          price_value: price,
          source_url: location.href,
          scraped_at: scrapedAt,
          source: "store77",
        });
      }

      return {
        products: result,
        cardsFound: cards.length,
        title: document.title,
      };
    },
    { scrapedAt },
  );

  console.error(
    `    Cards found: ${products.cardsFound}, products extracted: ${products.products.length}, title: ${products.title}`,
  );

  if (!products.products.length) {
    const debugPath = path.join(
      OUTPUT_DIR,
      `store77_debug_${Date.now()}.html`,
    );

    await fs.writeFile(debugPath, await page.content(), "utf8");
    console.error(`    Debug HTML saved to: ${debugPath}`);
  }

  return products.products;
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  const scrapedAt = new Date().toISOString();
  const browser = await chromium.launch({ headless: true });

  const page = await browser.newPage({
    userAgent:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    viewport: {
      width: 1440,
      height: 900,
    },
  });

  const productsByUrl = new Map();

  try {
    for (const [sectionIndex, sectionUrl] of STORE77_SECTIONS.entries()) {
      console.error(
        `[store77 ${sectionIndex + 1}/${STORE77_SECTIONS.length}] ${sectionUrl}`,
      );

      const pages = await discoverPages(page, sectionUrl);

      for (const [pageIndex, currentPageUrl] of pages.entries()) {
        const before = productsByUrl.size;

        const products = await scrapePage(
          page,
          currentPageUrl,
          scrapedAt,
        );

        for (const product of products) {
          productsByUrl.set(normalizeUrl(product.url), product);
        }

        console.error(
          `  page ${pageIndex + 1}/${pages.length}: +${
            productsByUrl.size - before
          }`,
        );
      }
    }
  } finally {
    await browser.close();
  }

  const products = [...productsByUrl.values()].sort((a, b) =>
    a.url.localeCompare(b.url),
  );

  const datedPath = path.join(
    OUTPUT_DIR,
    `store77_products_${todayStamp()}.json`,
  );

  const latestPath = path.join(
    OUTPUT_DIR,
    "store77_products_latest.json",
  );

  const content = JSON.stringify(products, null, 2) + "\n";

  await fs.writeFile(datedPath, content, "utf8");
  await fs.writeFile(latestPath, content, "utf8");

  console.error(
    `Done store77: ${products.length} unique products saved to ${latestPath}`,
  );

  console.log(latestPath);
}

main().catch((error) => {
  console.error(error?.stack || error);
  process.exit(1);
});