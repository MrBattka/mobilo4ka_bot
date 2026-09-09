import re
from typing import Any

from normalizers_site.ban_words import ban_word


def _replace_once(value: str, old: str, new: str) -> str:
    return value.replace(old, new, 1)


def _move_cn_to_start(value: str) -> str:
    value = value.strip()
    match = re.match(r"^(.*?)(?:\s+)?(CN|🇨🇳)$", value)

    if not match:
        return value

    return f"{match.group(2)} {match.group(1).strip()}".strip()


def return_fix_name_trubkoved(name: Any) -> str:
    value = _move_cn_to_start(str(name or ""))

    replacements = [
        ("Gb", ""),
        ("GB", ""),
        ("Space Black", "Black"),
        ("Space Gray", "Gray"),
        ("Lavander", "Lavender"),
        ("Z Fold6", "Z Fold 6"),
        ("Z Flip6", "Z Flip 6"),
        ("Z Fold7", "Z Fold 7"),
        ("Z Flip7", "Z Flip 7"),
        ("Magic Mouse (USB-C)", "Magic Mouse 3"),
        ("Wi‑Fi", "Wi-Fi"),
        ("(M4)", "M4"),
        ("(M3)", "M3"),
        ("(M5)", "M5"),
        ("SE (2024)", "SE2"),
        ("SE (2025)", "SE3"),
        ("SE 2 (2024)", "SE2"),
        ("SE 3 (2025)", "SE3"),
        ("mm", ""),
        ("Yandex", "Яндекс"),
        ("Disk", "Disc"),
        ("/1024 ", "/1TB "),
        ("zflip", "z flip"),
        ("Wi-Fi + LTE", "5G"),
        ("s26 Plus", "S26+"),
        ("s25 Plus", "S25+"),
        ("128 ГБ,", "128"),
        ("256 ГБ", "256"),
        ("512 ГБ", "512"),
        ("1 ТБ", "1TB"),
        ("2 ТБ", "2TB"),
        ("SE 3", "SE3"),
        ("Apple Watch Series 11", "S11"),
        ("CN", "🇨🇳"),
        ('Air 13"', "Air 13"),
        ('Air 13"', "Air 11"),
        (" ТБ,", "TB"),
        (" ГБ,", ""),
    ]

    for old, new in replacements:
        value = _replace_once(value, old, new)

    if "iPhone 16" in value:
        value = _replace_once(value, " nano SIM + eSIM,", "")
        value = _replace_once(value, " eSIM,", "")

    value = _replace_once(value, ",", "")
    value = _replace_once(value, " ГБ", "")

    if re.search(r"nano\s+sim\s+\+\s+esim", value, re.IGNORECASE):
        value = re.sub(
            r"nano\s+sim\s+\+\s+esim",
            "",
            value,
            count=1,
            flags=re.IGNORECASE,
        )
        value = re.sub(r",\s+", " ", value)
        value = re.sub(r"\s{2,}", " ", value).strip()
        value = f"nano SIM + eSIM {value}"

    if re.search(r"esim", value, re.IGNORECASE):
        value = re.sub(r"esim", "", value, count=1, flags=re.IGNORECASE)
        value = re.sub(r",\s+", " ", value)
        value = re.sub(r"\s{2,}", " ", value).strip()
        value = f"eSIM {value}"

    value = _replace_once(value, "eSIM nano SIM", "(Sim+eSim)")

    return value


def normalize_trubkoved_rows(rows: list[Any]) -> list[Any]:
    result = []

    for row in rows:
        if isinstance(row, dict):
            name = row.get("name", "")

            if ban_word(name):
                continue

            fixed_row = row.copy()
            fixed_row["name"] = return_fix_name_trubkoved(name)

            if not ban_word(fixed_row["name"]):
                result.append(fixed_row)

        elif isinstance(row, (list, tuple)) and row:
            name = row[0]

            if ban_word(name):
                continue

            fixed_row = list(row)
            fixed_row[0] = return_fix_name_trubkoved(name)

            if not ban_word(fixed_row[0]):
                result.append(fixed_row)

    return result