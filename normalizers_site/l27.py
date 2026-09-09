import re
from typing import Any


FLAGS = (
    "🇯🇵", "🇮🇳", "🇪🇺", "🇦🇪", "🇧🇷", "🇻🇳", "🇰🇼", "🇺🇸",
    "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺", "🇨🇦", "🇨🇱",
    "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿", "🇰🇷", "🇬🇺", "🇺🇲",
)


def _check_flags(value: str) -> str:
    value = value.rstrip()

    for flag in FLAGS:
        if value.endswith(flag):
            return f"{flag}{value[:-len(flag)].rstrip()}"

    return value


def fix_name_l27(name: Any) -> str:
    value = re.sub(r"\s+", " ", str(name or ""))

    replacements = [
        ("1T ", "1Tb "),
        ("1T\u00a0 ", "1Tb "),
        ("16Pro ", "16 Pro "),
        ("16Pro\u00a0 ", "16 Pro "),
        ("15Pro ", "15 Pro "),
        ("15Pro\u00a0", "15 Pro "),
        ("17Pro ", "17 Pro "),
        ("16+ ", "16 Plus "),
        ("15+ ", "15 Plus "),
        ("14+ ", "14 Plus "),
        ("15+\u00a0 ", "15 Plus "),
        ("16+\u00a0 ", "16 Plus "),
        ("14Pro ", "14 Pro "),
        ("12Pro\u00a0 ", "12 Pro "),
        ("Maus ", "Mouse "),
        ("Mause", "Mouse"),
        ("SE 2024", "SE2"),
        (" 2T ", " 2Tb "),
        ("АirPods", "AirPods"),
        ("17е", "17e"),
    ]

    for old, new in replacements:
        value = value.replace(old, new)

    return re.sub(r"\s+", " ", value).strip()


def return_name_in_arr_l27(name: Any) -> str:
    value = _check_flags(str(name or ""))[::-1]

    if " " in value:
        value = value.split(" ", 1)[1]

    return fix_name_l27(value[::-1])


def return_stock_price_l27(name: Any) -> str:
    value = str(name or "")

    for flag in FLAGS:
        value = value.replace(flag, "")

    value = value[::-1].lstrip(" \u00a0")

    price = re.split(r"[ \u00a0]", value, maxsplit=1)[0]
    return price[::-1]


def return_extra_price_l27(name: Any) -> Any:
    product_name = return_name_in_arr_l27(name)
    price = return_stock_price_l27(name)

    return price


def normalize_l27_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    name = return_name_in_arr_l27(raw_value)

    price = (
        str(row[1]).strip()
        if len(row) > 1 and row[1] not in ("", None)
        else return_stock_price_l27(raw_value)
    )

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]