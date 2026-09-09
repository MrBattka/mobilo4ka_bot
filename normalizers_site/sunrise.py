import re
from typing import Any


def fix_name_sunrise(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("🔌", ""),
        ("mm", ""),
        ("Gb", ""),
        ("GB", ""),
        ("🔥", ""),
        ("⚡️", ""),
        ("S8 2022", "S8"),
        ("S9 2023", "S9"),
        ("SE 2024", "SE2"),
        ("/1 ", "/1TB "),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    return re.sub(r"\s+", " ", value).strip()


def return_name_in_arr_sunrise(name: Any) -> str:
    value = str(name or "").strip()

    # Название находится до разделителя "-"
    if "-" in value:
        value = value.rsplit("-", 1)[0]

    return fix_name_sunrise(value)


def return_stock_price_sunrise(name: Any) -> str:
    value = str(name or "").strip()

    # Цена находится после последнего "-"
    if "-" not in value:
        return ""

    price = value.rsplit("-", 1)[1]
    price = re.sub(r"\D", "", price)

    return price if len(price) >= 5 else ""


def normalize_sunrise_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    name = return_name_in_arr_sunrise(raw_value)

    price = (
        str(row[1]).strip()
        if len(row) > 1 and row[1] not in ("", None)
        else return_stock_price_sunrise(raw_value)
    )

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]