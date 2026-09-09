import re
from typing import Any


FLAGS = (
    "🇯🇵", "🇮🇳", "🇪🇺", "🇦🇪", "🇧🇷", "🇻🇳", "🇰🇼", "🇺🇸",
    "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺", "🇨🇦", "🇨🇱",
    "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿", "🇰🇷", "🇬🇺", "🇮🇩",
    "🇿🇦", "🇵🇾",
)


def _strip_markdown(value: str) -> str:
    return re.sub(r"^(\*+|_+|`+)|(\*+|_+|`+)$", "", value.strip())


def _remove_flags(value: str) -> str:
    for flag in FLAGS:
        value = value.replace(flag, "")
    return value


def _extract_flag(value: str) -> tuple[str, str]:
    value = value.strip()
    flag_match = re.search(rf"({'|'.join(re.escape(f) for f in FLAGS)})\s*$", value)
    if flag_match:
        flag = flag_match.group(1)
        value = value[:flag_match.start()].rstrip()
        return value, flag
    return value, ""


def _strip_price_tail(value: str) -> str:
    value = _strip_markdown(value)
    value = _remove_flags(value).strip()
    value = re.sub(r"\s*(?:\((?:esim|2sim)\))?\s*$", "", value, flags=re.I)
    value = re.sub(r"(?<=\d)[A-Za-z₽€£$%]+$", "", value)
    return value.strip()


def fix_name_f51(name: Any) -> str:
    value = str(name or "")
    value = _strip_markdown(value)

    replacements = [
        ("Gb", ""),
        ("GB", ""),
        ("4G", ""),
        ("1T ", "1Tb "),
        ("S24 +", "S24+"),
        ("A05s 4/05", "A05s 4/64"),
        ("Nord CE 3", "Nord CE3"),
        ("Lavander", "Lavender"),
        ("Pnk", "Pink"),
        ("mm", ""),
        ("FE+", "FE +"),
        ("Grey", "Gray"),
        ("CE 5", "CE5"),
        ("CE 4", "CE4"),
        ("ACE5", "Ace 5"),
        ("Slver", "Silver"),
        ("Siver", "Silver"),
        ("Ace5", "Ace 5"),
        ("Brow", "Brown"),
        ("Sony Xperia", "Dual 🇭🇰 Sony Xperia"),
        ("Sony  Xperia", "Dual 🇭🇰 Sony Xperia"),
        ("Yelow", "Yellow"),
        ("Greem", "Green"),
        ("8.7 ", ""),
        ("Pad SE6", "Pad SE 6"),
        ("Parcelain", "Porcelain"),
        ("A9+", "A9 +"),
        ("S9+", "S9 +"),
        ("S9 + FE", "S9 FE +"),
        ("Wi-Fi ", ""),
        ("Red Magic 9 PRO", "RedMagic 9 Pro"),
        ("1512", "512"),
        ("1256", "256"),
        ("1128", "128"),
        ("512G", "512"),
        ("256G", "256"),
        ("128G", "128"),
        ("S10+", "S10 +"),
        ("Samsung Buds", "Galaxy Buds"),
        ("Limongrass", "Lemongrass"),
        (" bsidian", "Obsidian"),
        ("Obsidain", "Obsidian"),
        ("Nothing Watch PRO", "CMF Watch PRO"),
        ("Red Magic", "RedMagic"),
        ("Geen", "Green"),
        ("PRO", "Pro"),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    if "Tab S" in value:
        value = value.replace("5G", "LTE", 1)

    # if "Pixel" in value:
    #     for memory in ("8/", "6/", "12/", "16/"):
    #         value = value.replace(memory, "", 1)

    if "Redmi Pad" in value:
        value = value.replace("LTE ", "", 1)
        value = value.replace("5G ", "", 1)
        value = value.replace("Wi-Fi ", "", 1)

    if "Tab " in value:
        value = value.replace("A9+", "A9 +", 1)
        value = value.replace("S9+", "S9 +", 1)
        value = value.replace("Wi-Fi ", "", 1)

    if "mi 12" in value:
        value = value.replace("Gray", "Black", 1)

    if "S23 FE" in value:
        value = value.replace("Gray", "Graphite", 1)

    if "Note 15 Pro" in value:
        value = value.replace("Silver", "Titan", 1)

    return re.sub(r"\s+", " ", value).strip()


def return_stock_price_f51(name: Any) -> str:
    value = str(name or "").strip()
    value = _strip_markdown(value)

    base, flag = _extract_flag(value)
    base = _strip_price_tail(base)

    match = re.search(r"(\d{5,7})\s*$", base)
    if not match:
        return ""

    return match.group(1)


def return_name_in_arr_f51(name: Any) -> str:
    value = str(name or "").strip()
    value = _strip_markdown(value)

    base, flag = _extract_flag(value)
    base = _strip_price_tail(base)

    name_part = re.sub(r"\s*\d{5,7}\s*$", "", base).strip()
    name_part = fix_name_f51(name_part)

    if flag:
        name_part = f"{name_part} {flag}".strip()

    return name_part


def return_extra_price_f51(name: Any) -> Any:
    return return_stock_price_f51(name)


def normalize_f51_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    if len(row) > 1 and row[1] not in ("", None):
        clean_name = _strip_markdown(raw_value)
        clean_name = _remove_flags(clean_name).strip()
        name = fix_name_f51(clean_name)
        price = str(row[1]).strip()
    else:
        name = return_name_in_arr_f51(raw_value)
        price = return_stock_price_f51(raw_value)

    price_digits = re.sub(r"\D", "", price)
    if len(price_digits) < 5:
        return []

    return [name, price]