import re
from typing import Any


FLAGS = (
    "🇯🇵", "🇮🇳", "🇪🇺", "🇦🇪", "🇧🇷", "🇻🇳", "🇰🇼", "🇺🇸",
    "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺", "🇨🇦", "🇨🇱",
    "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿", "🇰🇷", "🇿🇦", "🇵🇾",
    "🇮🇩",
)


def _remove_s5_service_parts(value: str) -> str:
    for item in FLAGS:
        value = value.replace(item, "")

    for item in (
        "1Sim+Esim",
        "🚘",
        "Buds 3 White",
        "Tab S9FE 8/256 Lavender 5G",
        "(2024)",
        "Loop",
        "1сим+есим",
        "(пленка)",
        "(esim)",
        "(2sim)",
    ):
        value = value.replace(item, "")

    return value


def _move_suffix(value: str) -> str:
    value = value.rstrip()

    for suffix in (*FLAGS, "(esim)", "(2sim)"):
        if value.endswith(suffix):
            return suffix + value[:-len(suffix)].rstrip()

    return value


def fix_name_s5(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("🎧", ""),
        ("✏️", ""),
        ("(после обмена)", ""),
        ("(2-sim)", ""),
        ("(пред актив)", ""),
        ("S/M", ""),
        ("M/L", ""),
        ("(наша вилка)", ""),
        ("1 TB", "1TB"),
        ("GB", ""),
        ("Gb", ""),
        ("S24FE", "S24 FE"),
        ("mm", ""),
        ("Starilgt ", "Starlight"),
        ("Grey ", "Gray"),
        ("Air Pods", "AirPods"),
        ("13 128  starting", "13 128 Starlight"),
        (" M4 2024", " M4"),
        ("M4 2024", "M4"),
        ("Space Gray", "Gray"),
        ("9 64 Grey", "9 64 Gray"),
        ("Pro Plus", "Pro +"),
        (" 4G", ""),
        ("A9+", "A9 +"),
        ("AirPods Pro MagSafe 2", "AirPods Pro 2"),
        ("S9 Plus", "S9 +"),
        ("iPad 10.2", "iPad 10"),
        ("MM", ""),
        ("A9 128", "Tab A9 128"),
        ("A9 + 128", "Tab A9 + 128"),
        ("FE+", "FE +"),
        ("S9FE", "S9 FE"),
        ("starling", "starlight"),
        ("S 10", "S10"),
        ("S23FE", "S23 FE"),
        ("Tab S10FE", "Tab S10 FE"),
        ("Tab S10 Plus", "Tab S10 +"),
        ("FE Plus", "FE +"),
        ("А55 ", "A55 "),
        ("Ice blue", "iceblue"),
        ("(e-sim)", "(esim)"),
        ("(2-sim)", "(2sim)"),
        ("2 TB", "2TB"),
        ("Starting", "Starlight"),
        ("S25 Plus", "S25+"),
        ("S25FE", "S25 FE"),
    ]

    for old, new in replacements:
        value = value.replace(old, new)

    if "S25 edge" in value:
        value = value.replace("256", "12/256", 1)
        value = value.replace("512", "12/512", 1)

    if "Tab S10" in value:
        value = value.replace("128", "8/128", 1)
        value = value.replace("256", "12/256", 1)

    if "35" in value:
        value = value.replace("ice blue", "iceblue")

    if "Pro Plus" in value and "5G" in value:
        value = value.replace("Pro Plus", "Pro Plus 5G", 1)

    return re.sub(r"\s+", " ", _move_suffix(value)).strip()


def return_stock_price_s5(name: Any) -> str:
    value = _remove_s5_service_parts(str(name or ""))
    match = re.search(r"(\d[\d\s]*)\s*$", value)

    if not match:
        return ""

    return re.sub(r"\s+", "", match.group(1))


def return_name_in_arr_s5(name: Any) -> str:
    value = fix_name_s5(name)

    price = return_stock_price_s5(value)
    if price:
        value = re.sub(rf"\s*{re.escape(price)}\s*$", "", value)

    value = re.sub(r"\s+", " ", value).strip()
    return value


def return_extra_price_s5(name: Any) -> Any:
    product_name = return_name_in_arr_s5(name)
    price = return_stock_price_s5(name)

    return price


def normalize_s5_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    name = return_name_in_arr_s5(raw_value)

    price = (
        str(row[1]).strip()
        if len(row) > 1 and row[1] not in ("", None)
        else return_stock_price_s5(raw_value)
    )

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]