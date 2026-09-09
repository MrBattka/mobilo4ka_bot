from typing import Any

from normalizers_site.ban_words import ban_word


def _replace_once(value: str, old: str, new: str) -> str:
    return value.replace(old, new, 1)


def return_fix_name_store77(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("Gb", ""),
        ("GB", ""),
        ("Space Black", "Black"),
        ("Space Gray", "Gray"),
        ("Черный", "Black"),
        ("Серебристый", "Silver"),
        ("Wi-Fi + Сотовая связь", "5G"),
        ("Голубой", "Blue "),
        ("Розовый", "Pink"),
        ("Желтый", "Yellow"),
        ("Фиолетовый", "Purple"),
        ("Серый", "Gray"),
        ("Сияющая звезда", "Starlight "),
        ("1 ТБ", "1TB"),
        ("1 TБ", "1TB"),
        ("2 ТБ", "2TB"),
        ("2 TБ", "2TB"),
        (" М2 ", "M2"),
        (" М3 ", "M3"),
        (" М4 ", "M4"),
        (" М5 ", "M5"),
        ("iPad mini (2024)", "iPad mini 7"),
    ]

    for old, new in replacements:
        value = _replace_once(value, old, new)

    return value


def normalize_store77_rows(rows: list[Any]) -> list[Any]:
    result = []

    for row in rows:
        if isinstance(row, dict):
            name = row.get("name", "")

            if ban_word(name):
                continue

            fixed_row = row.copy()
            fixed_row["name"] = return_fix_name_store77(name)

            if not ban_word(fixed_row["name"]):
                result.append(fixed_row)

        elif isinstance(row, (list, tuple)) and row:
            name = row[0]

            if ban_word(name):
                continue

            fixed_row = list(row)
            fixed_row[0] = return_fix_name_store77(name)

            if not ban_word(fixed_row[0]):
                result.append(fixed_row)

    return result