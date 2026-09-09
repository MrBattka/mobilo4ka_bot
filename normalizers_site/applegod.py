import re
from typing import Any
from normalizers_site.ban_words import ban_word

def _normalize_iphone_name(value: str) -> str:
    has_esim = bool(re.search(r"\be[\s-]?sim\b", value, re.IGNORECASE))
    has_dual_sim = bool(
        re.search(r"\bdual[\s-]?sim\b", value, re.IGNORECASE)
    )

    # Запоминаем английский цвет из скобок
    english_colors = re.findall(
        r"\(([A-Za-z][A-Za-z -]*)\)",
        value,
    )

    # Удаляем описания в скобках
    value = re.sub(r"\([^)]*\)", " ", value)

    # Удаляем eSim и Dual Sim из исходного места
    value = re.sub(
        r"\be[\s-]?sim\b|\bdual[\s-]?sim\b",
        " ",
        value,
        flags=re.IGNORECASE,
    )

    # Удаляем русские описания и служебные слова
    value = re.sub(
        r"\b(?:телефон|apple|iphone|цвет|гб|gb)\b",
        " ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"[А-ЯЁа-яё]+", " ", value)

    # Память
    value = re.sub(
        r"(\d+)\s*(?:тб|tb)\b",
        r"\1TB",
        value,
        flags=re.IGNORECASE,
    )

    # Лишние символы
    value = re.sub(r"[(),:;\"«»]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    # Добавляем английский цвет
    if english_colors:
        value = f"{value} {' '.join(english_colors)}"

    # Убираем повторяющиеся соседние слова: Black Black -> Black
    words = value.split()
    unique_words = []

    for word in words:
        if not unique_words or word.casefold() != unique_words[-1].casefold():
            unique_words.append(word)

    value = " ".join(unique_words)

    if has_dual_sim:
        suffix = "dual sim"
    elif has_esim:
        suffix = "esim"
    else:
        suffix = "sim+esim"

    return f"{value} {suffix}".strip()

def _replace_once(value: str, old: str, new: str) -> str:
    return value.replace(old, new, 1)


def return_fix_name_apple_god(name: Any) -> str:
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
        ("iPad Mini (2024)", "iPad mini 7"),
        ("Watch Series 11", "S11"),
        ("Watch Series 10", "S10"),
        ("Watch Series 9", "S9"),
        ("Tab S10+", "Tab S10 +"),
        ("Tab A9+", "Tab A9 +"),
        # Оставлено как в исходном JS
        ("Tab S10+", "Tab S11 +"),
        ("Tab S9 FE+", "Tab S9 FE +"),
        ("M4(2024)", "M4"),
        ('Pro 13"M4', "Pro 13 M4"),
        ('10.2" (2021)', "10"),
        ("M4(2026)", "M4"),
        ('Air 11"M4', "Air 11 M4"),
        ("Сияющая Звезда", "Starlight"),
        ('Pro 12.9" M2 (2022)', "Pro 13 M2"),
        ("1 TB", "1TB"),
        ("Wi-Fi+Cellular", "LTE"),
        ("ГБ, цвет: ", ""),
        (", цвет: : ", ""),
        ("Deep Blue", "Blue"),
        ("Mist Blue", "Blue"),
        ("Cloud White", "White"),
        ("Sky Blue", "Blue"),
        ("Бежевый", "Beige"),
        ("Лаванда", "Lavender"),
        ("Зеленый", "Green"),
        ("Оранжевый", "Orange"),
        ("Синий", "Blue"),
        ("Персиковый", "Peach"),
        ("Белый", "White"),
        (" ГБ", ""),
        ("2 TB", "2TB"),
        
    ]

    for old, new in replacements:
        value = _replace_once(value, old, new)
        
    if re.search(r"\b(?:apple\s+)?iphone\b", value, re.IGNORECASE):
        value = _normalize_iphone_name(value)

    if "Tab A9" in value:
        value = _replace_once(value, "Графит", "Black")

    if "S9 FE" in value:
        value = _replace_once(value, "Графит", "Gray")
        value = _replace_once(value, "Лаванда", "Purple")

    value = _replace_once(value, "Темно-синий", "Navy")
    value = _replace_once(value, "Мятный", "Mint")
    value = _replace_once(value, "Серебро", "Silver")

    replacements = [
        ("ZFlip7", "Z Flip 7"),
        ("Z Flip7", "Z Flip 7"),
        ("ZFold7", "Z Fold 7"),
        ("Z Fold7", "Z Fold 7"),
        ("ZFlip8", "Z Flip 8"),
        ("Z Flip8", "Z Flip 8"),
        ("ZFold8", "Z Fold 8"),
        ("Z Fold8", "Z Fold 8"),
        ("ZFlip6", "Z Flip 6"),
        ("Z Flip6", "Z Flip 6"),
        ("ZFold6", "Z Fold 6"),
        ("Z Fold6", "Z Fold 6"),
    ]

    for old, new in replacements:
        value = _replace_once(value, old, new)
        
    value = re.sub(r"\s*\(([^()]*)\)", r" \1", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value

def normalize_applegod_rows(rows: list[Any]) -> list[Any]:
    result = []

    for row in rows:
        if isinstance(row, dict):
            name = row.get("name", "")

            if ban_word(name):
                continue

            fixed_row = row.copy()
            fixed_row["name"] = return_fix_name_apple_god(name)

            if not ban_word(fixed_row["name"]):
                result.append(fixed_row)

        elif isinstance(row, (list, tuple)) and row:
            name = row[0]

            if ban_word(name):
                continue

            fixed_row = list(row)
            fixed_row[0] = return_fix_name_apple_god(name)

            if not ban_word(fixed_row[0]):
                result.append(fixed_row)

    return result