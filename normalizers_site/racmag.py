import re
from typing import Any


def return_fix_name_racmag(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("Gb", ""),
        ("GB", ""),
        ("4G ", ""),
        ("Pro+", "Pro +"),
        ("Redmi 14С", "Redmi 14C"),
        ("X8D ", "Honor X8D"),
        ("X8d ", "Honor X8D"),
        ("Lavander", "Lavender"),
        ("Bluе", "Blue"),
        ("Awesome ", ""),
        ("SE 8.7", "SE"),
        ("15С", "15C"),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    if (
        "400 8/" in value
        or "400 12/" in value
        or "400 Pro" in value
    ):
        value = value.replace("400", "Honor 400", 1)

    if "Note " in value:
        value = value.replace("Ice Blue", "Blue", 1)
        value = value.replace("Midnight ", "", 1)
        value = value.replace("Mint ", "", 1)
        value = value.replace("Forest ", "", 1)
        value = value.replace("Lavender ", "", 1)

    if "Note 14 Pro +" in value:
        value = value.replace("5G ", "", 1)

    return re.sub(r"\s+", " ", value).strip()


def return_name_in_arr_racmag(name: Any) -> str:
    value = str(name or "").strip()

    # Удаляем последнюю часть строки — цену
    parts = value.rsplit(maxsplit=1)
    return parts[0] if len(parts) > 1 else value


def return_stock_price_racmag(name: Any) -> str:
    value = str(name or "").strip()
    return value.rsplit(maxsplit=1)[-1] if value else ""


def return_extra_price_racmag(name: Any) -> Any:
    product_name = return_fix_name_racmag(
        return_name_in_arr_racmag(name)
    )
    price = return_stock_price_racmag(name)

    return price


def normalize_racmag_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    # Если цена уже находится в отдельной колонке
    if len(row) > 1 and row[1] not in ("", None):
        name = return_fix_name_racmag(raw_value)
        price = str(row[1]).strip()
    else:
        name = return_fix_name_racmag(return_name_in_arr_racmag(raw_value))
        price = return_stock_price_racmag(raw_value)

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]