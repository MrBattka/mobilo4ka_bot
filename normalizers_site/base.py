import re
from typing import Any


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _strip_markdown(value: str) -> str:
    return re.sub(r"^(\*+|_+|`+)|(\*+|_+|`+)$", "", value.strip())


def fix_name_base(name: Any) -> str:
    value = _strip_markdown(_clean(name))

    replacements = [
        ("GB", ""),
        ("Gb", ""),
        ("4G", ""),
        ("5G ", ""),
        ("5G", ""),
        ("LTE ", ""),
        ("Wi-Fi ", ""),
        ("WiFi ", ""),
        ("A53 5G", "A53"),
        ("A55 5G", "A55"),
        ("A35 5G", "A35"),
        ("A25 5G", "A25"),
        ("A26 5G", "A26"),
        ("A36 5G", "A36"),
        ("A56 5G", "A56"),
        ("A57 5G", "A57"),
        ("A37 5G", "A37"),
        ("Pocophone", "Poco"),
        ("Nord CE 3", "Nord CE3"),
        ("Apple Watch 10", "S10"),
        ("Apple Watch 9", "S9"),
        ("iPhone 14 +", "iPhone 14 Plus"),
        ("iPhone 16 +", "iPhone 16 Plus"),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    value = re.sub(r"\s+", " ", value).strip()

    if value.endswith(" +"):
        value = value[:-2] + " Plus"

    if value.startswith("Note ") and "4G" in value:
        value = value.replace("4G ", "", 1)

    return value.strip()


def _extract_price(raw_price: Any) -> str:
    value = _clean(raw_price)
    if not value:
        return ""

    value = value.replace(" ", "").replace("₽", "").replace("RUB", "")
    value = value.replace("€", "").replace("$", "").replace("£", "")

    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")

    value = re.sub(r"[^0-9.]", "", value)
    if not value:
        return ""

    return value.strip()


def normalize_base(row: list[Any]) -> list[Any]:
    if not row:
        return []

    if len(row) >= 4:
        name_raw = row[2]
        price_raw = row[3]
    elif len(row) >= 2:
        name_raw = row[0]
        price_raw = row[1]
    else:
        return []

    name = fix_name_base(name_raw)
    price = _extract_price(price_raw)

    if not name:
        return []

    return [name, price]