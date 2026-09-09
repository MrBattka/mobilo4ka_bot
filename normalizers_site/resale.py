import re
from typing import Any


FLAGS = (
    "🇪🇺", "🇦🇪", "🇮🇳", "🇧🇷", "🇯🇵", "🇻🇳", "🇰🇼", "🇺🇸",
    "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺", "🇨🇦", "🇨🇱",
    "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿", "🇰🇷",
)


def _remove_flags(value: str) -> str:
    for flag in FLAGS:
        value = value.replace(flag, "")
    return value


def return_name_resale(name: Any) -> str:
    """
    Возвращает название товара без цены и флагов.
    """
    value = _remove_flags(str(name or "")).strip()
    
    cleaned = re.sub(r"[—-]\s*\d+[\s₽]*\s*$", "", value).strip()
    
    # Если тире не было, пробуем просто удалить число в конце (менее надежно, но как fallback)
    cleaned = re.sub(r"\s\d+[\s₽]*\s*$", "", cleaned).strip()
    
    return cleaned.strip()


def return_stock_price_resale(name: Any) -> str:
    value = _remove_flags(str(name or "")).strip()

    # Сначала ищем цену в конце строки
    matches = re.findall(r"\d[\d\s]*", value)
    if not matches:
        return ""

    price = matches[-1].replace(" ", "")

    # Цена должна состоять минимум из пяти цифр
    return price if len(price) >= 5 else ""


def return_extra_price_resale(name: Any) -> Any:
    product_name = return_fix_name_resale(return_name_resale(name))
    price = return_stock_price_resale(name)

    return price


def return_fix_name_resale(name: Any) -> str:
    value = str(name or "")

    replacements = [
        (" с кейсом наша вилка", ""),
        (" наша вилка 🔌", ""),
        (" наша вилка", ""),
        (" с кейсом и чехлом", ""),
        (" с кейсом", ""),
        (" 🔌", ""),
        ("🔌", ""),
        ("Apple Watch Series ", "S"),
        ("🐭", ""),
        ("🎧", ""),
        ("✏️", ""),
        ("•", ""),
        ("Apple Watch ", ""),
        ("Lavander", "Lavender"),
        ("SM-", "SM"),
        ("G-", "G"),
        ("Type-C", "Type C"),
        ("1024", "1TB"),
        ("Sim-e", "Sim+e"),
        ("Fold5", "Fold 5"),
        ("Fold6", "Fold 6"),
        ("Wi-Fi + Cellular", "LTE"),
        ("SE 3 ", "SE3 "),
        ("S24 +", "S24+"),
        ("mm", ""),
        ("GB", ""),
        ("Flip5", "Flip 5"),
        ("VR2", "vr 2"),
        ("Flip6", "Flip 6"),
        ("Flip7", "Flip 7"),
        ("Fold7", "Fold 7"),
        ("Чёрный", "dualsense Black "),
        ("Белый", "dualsense White "),
        ("(3rd Gen)", "3"),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    # Исправления Apple Watch и iPhone
    if "SE" in value:
        value = value.replace("2 2023", " (2023) gen 2", 1)
        value = value.replace("Storm Blue", "Silver", 1)

    if "Ultra" in value:
        value = value.replace(" 49 ", " ", 1)
        value = value.replace("Green Gray", "Gray", 1)
        value = value.replace("Blue Black", "Black", 1)

    if "14 " in value:
        value = value.replace("Deep Purple", "Purple", 1)
        value = value.replace("Space Black", "Black", 1)

    if "SE3 " in value:
        value = value.replace("Midnight", "Black", 1)

    # 17 Pro / Pro Max: White → silver
    if re.search(r"17 Pro(?: Max)? (?:256|512|1TB|2TB)", value):
        value = value.replace("White", "silver", 1)

    # Убираем 5G у перечисленных моделей
    models = (
        "A25", "A26", "M35", "A36", "M56", "M55",
        "A55", "A56", "A57", "A37", "Note 14 Pro +", "S21",
    )

    if any(model in value for model in models):
        value = value.replace("5G ", "", 1)

    return re.sub(r"\s+", " ", value).strip()


def normalize_resale_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    # Если цена уже вынесена в отдельную колонку
    if len(row) > 1 and row[1] not in ("", None):
        name = return_fix_name_resale(raw_value)
        price = str(row[1]).strip()
    else:
        name = return_fix_name_resale(return_name_resale(raw_value))
        price = return_stock_price_resale(raw_value)

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]