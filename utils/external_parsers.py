import asyncio
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, List

BASE_DIR = Path(__file__).resolve().parent.parent
PARSER_DIR = BASE_DIR / "parserBoltunTrub"
OUTPUT_DIR = PARSER_DIR / "outputs"


def _latest_file(paths: Iterable[Path]) -> Path | None:
    candidates = [p for p in paths if p.exists()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _normalize_product_row(item: Any) -> List[Any] | None:
    if item is None:
        return None
    if isinstance(item, (list, tuple)):
        return [str(v) if v is not None else "" for v in item]
    if not isinstance(item, dict):
        return None

    name = str(item.get("name") or item.get("title") or "").strip()
    if not name:
        return None

    price_value = item.get("price_value")
    if price_value in (None, ""):
        raw_price = item.get("price") or item.get("price_rub") or item.get("value") or 0
        try:
            price_value = str(raw_price).replace(" ", "").replace("₽", "").replace(",", ".")
            price_value = float(price_value)
        except Exception:
            price_value = 0

    url = str(item.get("url") or item.get("link") or item.get("href") or "").strip()
    return [name, price_value, url]


def _normalize_rows(data: Any) -> List[List[Any]]:
    if data is None:
        return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []

    rows: List[List[Any]] = []
    for item in data:
        row = _normalize_product_row(item)
        if row:
            rows.append(row)
    return rows


def _read_json_products(path: Path) -> List[List[Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        return _normalize_rows(payload)
    except Exception:
        return []


def _read_csv_products(path: Path) -> List[List[Any]]:
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            rows: List[List[Any]] = []
            for row in reader:
                name = (row.get("name") or row.get("product") or "").strip()
                price = row.get("price") or row.get("cost") or ""
                url = row.get("url") or row.get("link") or ""
                if name:
                    rows.append([name, price, url])
            return rows
    except Exception:
        return []


def _run_script_checked(script_name: str, command: list[str], timeout: int = 180) -> bool:
    script_path = PARSER_DIR / script_name
    if not script_path.exists():
        return False

    try:
        result = subprocess.run(
            command,
            cwd=str(PARSER_DIR),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        return True
    except subprocess.TimeoutExpired:
        print(f"⚠️ {script_name}: timeout after {timeout}s")
        return False
    except Exception as e:
        print(f"⚠️ {script_name}: launch error: {e}")
        return False


async def run_parser_boltun() -> List[List[Any]]:
    _run_script_checked("scrape_boltyn.mjs", ["node", "scrape_boltyn.mjs"], timeout=180)

    latest = _latest_file([
        OUTPUT_DIR / "boltyn_products_latest.json",
        OUTPUT_DIR / "boltyn_products_2026-08-18.json",
    ])

    if latest is None:
        return []

    if latest.suffix.lower() == ".json":
        return _read_json_products(latest)

    if latest.suffix.lower() == ".csv":
        return _read_csv_products(latest)

    return []

async def run_parser_applegod() -> List[List[Any]]:
    success = await asyncio.to_thread(
        _run_script_checked,
        "scrape_applegod.mjs",
        ["node", "scrape_applegod.mjs"],
        800,
    )

    latest = OUTPUT_DIR / "applegod_products_latest.json"

    if not success or not latest.exists():
        return []

    return _read_json_products(latest)

async def run_parser_store77() -> List[List[Any]]:
    success = await asyncio.to_thread(
        _run_script_checked,
        "scrape_store77.mjs",
        ["node", "scrape_store77.mjs"],
        800,
    )

    latest = OUTPUT_DIR / "store77_products_latest.json"

    if not success or not latest.exists():
        return []

    return _read_json_products(latest)


async def run_parser_trubkoved(max_sections: int = 2, delay: float = 2.0) -> List[List[Any]]:
    _run_script_checked("scrape_trubkoved.py", [sys.executable, "scrape_trubkoved.py"], timeout=180)

    latest = _latest_file([
        OUTPUT_DIR / "trubkoved_products_latest.json",
        OUTPUT_DIR / "trubkoved_products_2026-08-18.json",
        OUTPUT_DIR / "trubkoved_products_latest.csv",
        OUTPUT_DIR / "trubkoved_products_2026-08-18.csv",
    ])

    if latest is None:
        return []

    if latest.suffix.lower() == ".json":
        return _read_json_products(latest)

    if latest.suffix.lower() == ".csv":
        return _read_csv_products(latest)

    return []