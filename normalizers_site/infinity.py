import re
from typing import Any


COUNTRY_FLAGS = (
    "🇯🇵", "🇮🇳", "🇪🇺", "🇦🇪", "🇧🇷", "🇻🇳", "🇰🇼",
    "🇺🇸", "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺",
    "🇨🇦", "🇨🇱", "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿",
    "🇰🇷", "🇬🇺", "🇿🇦",
)


def _move_suffix_to_start(value: str) -> str:
    value = value.rstrip()

    for suffix in (*COUNTRY_FLAGS, "eSIM", "dual", "(e-sim)", "(2-sim)"):
        if value.endswith(suffix):
            return suffix + value[:-len(suffix)].rstrip()

    return value


def fix_name_infinity(name: Any) -> str:
    value = str(name or "").strip()

    replacements = {
        "Pencil 1-gen (USB-C)": "Pencil USB C ",
        "Pencil (USB-C)": "Pencil USB C ",
        "1 TB": "1TB",
        "2 TB": "2TB",
        "Air Pods": "AirPods",
        "eSIM": "🇺🇸",
        "(e-sim)": "🇺🇸",
        "(2-sim)": "dual",
        "Starting": "Starlight",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    for symbol in ("🎧", "✏️", "🖱️", "💥"):
        value = value.replace(symbol, "")

    value = value.replace("Gb", "").replace("GB", "")
    value = value.replace("2sim", "")
    value = re.sub(r"\s+", " ", value).strip()

    value = _move_suffix_to_start(value)
    value = value.replace("Wi-Fi", "WiFi")

    # Убираем цену и служебный хвост после последнего разделителя.
    parts = value.rsplit(" ", 1)
    if len(parts) == 2 and re.search(r"\d", parts[1]):
        value = parts[0]

    value = value.replace("WiFi", "Wi-Fi")
    return re.sub(r"\s+", " ", value).strip()


def return_stock_price_infinity(name: Any) -> str:
    value = str(name or "")

    for flag in COUNTRY_FLAGS:
        value = value.replace(flag, "")

    value = re.sub(r"[🔥💥🎧✏️🖱️]", "", value)
    value = value.replace("(e-sim)", "").replace("2sim", "")
    value = value.replace("Buds 3 White", "")
    value = value.replace("Tab S9FE 8/256 Lavender 5G", "")
    value = value.replace("(2024)", "")

    # Берём последнее числовое значение как цену.
    prices = re.findall(r"\d[\d\s.,]*", value)
    if not prices:
        return ""

    price = prices[-1].replace(" ", "").replace("\u00a0", "")
    price = price.replace(",", ".")
    price = price.replace(".", "")
    return price


def normalize_infinity_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_name = str(row[0] or "").strip()
    if not raw_name:
        return []

    name = fix_name_infinity(raw_name)

    if len(row) > 1 and row[1] not in ("", None):
        price = row[1]
    else:
        price = return_stock_price_infinity(raw_name)

    return [name, price]