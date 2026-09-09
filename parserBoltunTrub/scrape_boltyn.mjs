import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = path.join(ROOT, "outputs");
const BOLTYN_SECTIONS = [
  "https://boltyn.ru/catalog/phones/",
  "https://boltyn.ru/catalog/planshety/",
  "https://boltyn.ru/catalog/accessorize/smart_braslety/",
  "https://boltyn.ru/catalog/accessorize/chasy/",
  "https://boltyn.ru/catalog/accessorize/naushniki_apple/",
  "https://boltyn.ru/catalog/accessorize/besprovodnye_naushniki/",
  "https://boltyn.ru/catalog/accessorize/provodnye_naushniki/",
  "https://boltyn.ru/catalog/accessorize/blutooth_garnitury/",
];

const MAX_PAGES = Number(process.env.BOLTYN_MAX_PAGES || "0");
const EMPTY_PAGE_LIMIT = Number(process.env.BOLTYN_EMPTY_PAGE_LIMIT || "6");

function todayStamp() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function pageUrl(sectionUrl, pageNumber) {
  if (pageNumber <= 1) return sectionUrl;
  return `${sectionUrl}?PAGEN_1=${pageNumber}`;
}

async function gotoWithRetry(page, url) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
      return;
    } catch (error) {
      const hasProducts = await page.locator(".product[data-id]").count().catch(() => 0);
      if (hasProducts > 0) return;
      if (attempt === 3) throw error;
      console.error(`  retry ${attempt}/3 after navigation issue: ${url}`);
      await page.waitForTimeout(3000 * attempt);
    }
  }
}

async function discoverPages(page, sectionUrl) {
  await gotoWithRetry(page, sectionUrl);
  await page.waitForTimeout(1500);
  const pageNumbers = await page.evaluate(() => {
    const numbers = new Set([1]);
    for (const anchor of document.querySelectorAll('a[href*="PAGEN_1="]')) {
      const match = anchor.href.match(/[?&]PAGEN_1=(\d+)/);
      if (match) numbers.add(Number(match[1]));
    }
    return Array.from(numbers).filter(Number.isFinite);
  });
  const maxPage = Math.max(1, ...pageNumbers);
  const limitedMaxPage = MAX_PAGES > 0 ? Math.min(maxPage, MAX_PAGES) : maxPage;
  return Array.from({ length: limitedMaxPage }, (_, index) => pageUrl(sectionUrl, index + 1));
}

async function scrapePage(page, url, scrapedAt) {
  await gotoWithRetry(page, url);
  await page.waitForTimeout(1000);

  return await page.evaluate(
    ({ scrapedAt }) => {
      function clean(text) {
        return String(text || "").replace(/\s+/g, " ").trim();
      }

      function absolute(href) {
        return new URL(href, location.origin).href;
      }

      const products = [];
      for (const card of document.querySelectorAll(".product[data-id]")) {
        if (!/в наличии/i.test(card.innerText || "")) continue;

        const priceNode = card.querySelector(".price[data-price]");
        const priceValue = Number(String(priceNode?.getAttribute("data-price") || "").replace(/\D+/g, ""));
        if (!Number.isFinite(priceValue) || priceValue <= 0) continue;

        const link = card.querySelector(".name a[href]");
        const href = link?.getAttribute("href") || "";
        const category = clean(card.querySelector(".cat")?.innerText || "");
        const title = clean(link?.innerText || "");
        const name = clean([category, title].filter(Boolean).join(" "));
        if (!name || !href) continue;

        products.push({
          name,
          url: absolute(href),
          price: `${priceValue}`,
          price_value: priceValue,
          source_url: location.href,
          scraped_at: scrapedAt,
          source: "boltyn",
        });
      }
      return products;
    },
    { scrapedAt },
  );
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  const scrapedAt = new Date().toISOString();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
  });

  const productsByUrl = new Map();
  try {
    for (const [sectionIndex, sectionUrl] of BOLTYN_SECTIONS.entries()) {
      console.error(`[boltyn ${sectionIndex + 1}/${BOLTYN_SECTIONS.length}] ${sectionUrl}`);
      const pages = await discoverPages(page, sectionUrl);
      let emptyPageStreak = 0;
      for (const [pageIndex, url] of pages.entries()) {
        const before = productsByUrl.size;
        const products = await scrapePage(page, url, scrapedAt);
        for (const product of products) productsByUrl.set(product.url, product);
        const added = productsByUrl.size - before;
        console.error(`  page ${pageIndex + 1}/${pages.length}: +${added}`);
        emptyPageStreak = added === 0 ? emptyPageStreak + 1 : 0;
        if (EMPTY_PAGE_LIMIT > 0 && emptyPageStreak >= EMPTY_PAGE_LIMIT) {
          console.error(`  stop section after ${emptyPageStreak} empty pages`);
          break;
        }
      }
    }
  } finally {
    await browser.close();
  }

  const products = Array.from(productsByUrl.values()).sort((a, b) => a.url.localeCompare(b.url));
  const stamp = todayStamp();
  const datedPath = path.join(OUTPUT_DIR, `boltyn_products_${stamp}.json`);
  const latestPath = path.join(OUTPUT_DIR, "boltyn_products_latest.json");

  if (products.length === 0) {
    const previousProducts = await readProducts(latestPath);
    if (previousProducts.length > 0) {
      console.error(
        `Done boltyn: 0 products, keeping previous latest with ${previousProducts.length} products`,
      );
      console.log(latestPath);
      return;
    }
  }

  await fs.writeFile(datedPath, JSON.stringify(products, null, 2) + "\n", "utf8");
  await fs.writeFile(latestPath, JSON.stringify(products, null, 2) + "\n", "utf8");
  console.error(`Done boltyn: ${products.length} unique products`);
  console.log(latestPath);
}

async function readProducts(filePath) {
  try {
    const rows = JSON.parse(await fs.readFile(filePath, "utf8"));
    return Array.isArray(rows) ? rows : [];
  } catch {
    return [];
  }
}

main().catch((error) => {
  console.error(error?.stack || error);
  process.exit(1);
});
