import re
from typing import Any


REMOVE_SYMBOLS = "🛩️🏎️🚙🚕🚚🚗🚘🚖🎧💻🍏"


def fix_name_hi(name: Any) -> str:
    """Аналог fixNameHi из helpers.js."""
    value = str(name or "")
    value = re.sub(r"\s+", " ", value).strip()

    if "Bot:" in value:
        value = value.split("Bot:", 1)[1]

    for symbol in REMOVE_SYMBOLS:
        value = value.replace(symbol, "")

    value = value.replace("⌨️", "Keyboard ")
    value = value.replace("0️", "0")

    replacements = {
        "USB-C": "USB-C",
        "TYPE-C": "USB-C",
        "WiFi": "Wi-Fi",
        "S24 +": "S24+",
        "S24 8/128 Gray": "S24 8/128 Marble Gray",
        "S24 8/128 Violet": "S24 8/128 Cobalt Violet",
        "S24 8/128 Yellow": "S24 8/128 Amber Yellow",
        "S24 8/128 Green": "S24 8/128 Jade Green",
        "S24 8/128 Orange": "S24 8/128 Sandstore Orange",
        "S24 8/256 Gray": "S24 8/256 Marble Gray",
        "S24 8/256 Violet": "S24 8/256 Cobalt Violet",
        "S24 8/256 Yellow": "S24 8/256 Amber Yellow",
        "S24 8/256 Black": "S24 8/256 Onyx Black",
        "S24 8/256 Green": "S24 8/256 Jade Green",
        "S24 8/256 Orange": "S24 8/256 Sandstone Orange",
        "S24 12/256 Gray": "S24 12/256 Marble Gray",
        "S24 12/256 Violet": "S24 12/256 Cobalt Violet",
        "S24 12/256 Yellow": "S24 12/256 Amber Yellow",
        "S24 12/256 Black": "S24 12/256 Onyx Black",
        "S24 12/256 Green": "S24 12/256 Jade Green",
        "S24 12/256 Orange": "S24 12/256 Sandstone Orange",
        "S24 12/512 Gray": "S24 12/512 Marble Gray",
        "S24 12/512 Violet": "S24 12/512 Cobalt Violet",
        "S24 12/512 Yellow": "S24 12/512 Amber Yellow",
        "S24+ 12/256 Gray": "S24+ 12/256 Marble Gray",
        "S24+ 12/256 Violet": "S24+ 12/256 Cobalt Violet",
        "S24+ 12/256 Yellow": "S24+ 12/256 Amber Yellow",
        "S24+ 12/256 Black": "S24+ 12/256 Onyx Black",
        "S24+ 12/256 Green": "S24+ 12/256 Jade Green",
        "S24+ 12/256 Orange": "S24+ 12/256 Sandstone Orange",
        "S24+ 12/512 Gray": "S24+ 12/512 Marble Gray",
        "S24+ 12/512 Violet": "S24+ 12/512 Cobalt Violet",
        "S24+ 12/512 Yellow": "S24+ 12/512 Amber Yellow",
        "S24+ 12/512 Black": "S24+ 12/512 Onyx Black",
        "Z Flip5": "Z Flip 5",
        "Z Flip6": "Z Flip 6",
        "Z Fold5": "Z Fold 5",
        "Z Fold6": "Z Fold 6",
        "Tab S9 5g 8/128": "Tab S9 8/128 lte",
        "Orange Beige": "Orange",
        "Green Gray": "Gray",
        "S9 +": "S9+",
        "FE +": "FE+",
        "Black Blue": "Blue/Black",
        "Ice Blue": "IceBlue",
        "Blue Black": "Blue/Black",
        "Grey": "Gray",
        "A15 5G": "A15",
        "A25 5G": "A25",
        "A35 5G": "A35",
        "A54 5G": "A54",
        "A55 5G": "A55",
        "16Е": "16e",
        "13C": "13c",
        "1024": "1Tb",
        "Watch4": "Watch 4",
        "Watch5": "Watch 5",
        "Watch6": "Watch 6",
        "Watch7": "Watch 7",
        "S 8 ": "S8 ",
        "S 9 ": "S9 ",
        "Light Green": "Green",
        "Light Violet": "Violet",
        "S24 8/128 Black": "S24 8/128 Onyx Black",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)
        
    value = re.sub(r'\s*-\s*\d+(\.\d+)?\s*\*\*', '', value)

    value = value.replace("mm", "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def return_stock_price_hi(text: Any) -> str:
    """Извлекает складскую цену после дефиса."""
    value = str(text or "")
    value = re.sub(r"\s+", " ", value).strip()

    if "-" in value:
        value = value.rsplit("-", 1)[1]

    value = re.sub(r"[^\d.,]", "", value)
    return value.replace(",", ".")


def normalize_hi_row(row: list[Any]) -> list[Any]:
    """
    Преобразует строку Hi в единый формат:
    [нормализованное название, цена].
    """
    if not row:
        return []

    raw_text = str(row[0] or "").strip()
    if not raw_text:
        return []

    name = fix_name_hi(raw_text)
    price = row[1] if len(row) > 1 and row[1] not in ("", None) else \
        return_stock_price_hi(raw_text)

    return [name, price]