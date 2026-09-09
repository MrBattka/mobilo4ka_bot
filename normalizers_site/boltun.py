import re
from typing import Any

from normalizers_site.ban_words import ban_word


def _replace_once(value: str, old: str, new: str) -> str:
    return value.replace(old, new, 1)


def return_fix_name_boltun(name: Any) -> str:
    value = str(name or "")
    value = re.sub(r"\s+", " ", value)

    replacements = [
        ("Gb", ""),
        ("GB", ""),
        (" Dua ", " Dual "),
        ("Space Black", "Black"),
        ("Space Gray", "Gray"),
        ("nano SIM + eSIM ", ""),
        ("Narural", "Natural"),
        ("Sony Xperia", "Dual 🇭🇰 Sony Xperia"),
        ("Tab S10+", "Tab S10 +"),
        ("17 256 eSim", "eSim 17 256"),
        ("17 512 eSim", "eSim 17 512"),
        ("17 256 Nano Sim + eSim", "Sim + eSim 17 256"),
        ("17 512 Nano Sim + eSim", "Sim + eSim 17 512"),
        ("17 Pro 256 eSim", "eSim 17 Pro 256"),
        ("17 Pro 512 eSim", "eSim 17 Pro 512"),
        ("17 Pro 1Tb eSim", "eSim 17 Pro 1Tb"),
        ("17 Pro 256 Nano Sim + eSim", "Sim + eSim 17 Pro 256"),
        ("17 Pro 512 Nano Sim + eSim", "Sim + eSim 17 Pro 512"),
        ("17 Pro 1Tb Nano Sim + eSim", "Sim + eSim 17 Pro 1Tb"),
        ("17 Pro Max 256 eSim", "eSim 17 Pro Max 256"),
        ("17 Pro Max 512 eSim", "eSim 17 Pro Max 512"),
        ("17 Pro Max 1Tb eSim", "eSim 17 Pro Max 1Tb"),
        ("17 Pro Max 2Tb eSim", "eSim 17 Pro Max 2Tb"),
        ("17 Pro Max 256 Nano Sim + eSim", "Sim + eSim 17 Pro Max 256"),
        ("17 Pro Max 512 Nano Sim + eSim", "Sim + eSim 17 Pro Max 512"),
        ("17 Pro Max 1Tb Nano Sim + eSim", "Sim + eSim 17 Pro Max 1Tb"),
        ("17 Pro Max 1TB Nano Sim + eSim", "Sim + eSim 17 Pro Max 1TB"),
        ("17 Pro Max 2Tb Nano Sim + eSim", "Sim + eSim 17 Pro Max 2Tb"),
        ("17 Pro Max 2TB Nano Sim + eSim", "Sim + eSim 17 Pro Max 2TB"),
    ]

    for old, new in replacements:
        value = _replace_once(value, old, new)

    value = _replace_once(value, "Nano Sim + eSim", "🇮🇳")
    value = _replace_once(value, "Silver", "White")
    value = _replace_once(value, "Black", "Gray")

    value = _replace_once(value, "CE 5", "CE5")

    if "S25 " in value:
        value = _replace_once(value, "White", "Silver")

    if "iPhone" in value and "17 Pro" in value:
        value = _replace_once(value, "White", "Silver")

    return value


def normalize_boltun_rows(rows: list[Any]) -> list[Any]:
    result = []

    for row in rows:
        if isinstance(row, dict):
            name = row.get("name", "")

            if ban_word(name):
                continue

            fixed_row = row.copy()
            fixed_row["name"] = return_fix_name_boltun(name)

            if not ban_word(fixed_row["name"]):
                result.append(fixed_row)

        elif isinstance(row, (list, tuple)) and row:
            name = row[0]

            if ban_word(name):
                continue

            fixed_row = list(row)
            fixed_row[0] = return_fix_name_boltun(name)

            if not ban_word(fixed_row[0]):
                result.append(fixed_row)

    return result