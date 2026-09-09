import re
from typing import Any


def _get_price_vsemi(name: Any) -> str:
    """Извлекает цену из конца строки."""
    value = str(name or "").strip()
    # Ищем число в конце строки, возможно перед ним есть дефис и пробелы
    # Паттерн: опционально пробелы, опционально дефис, пробелы, цифры, конец строки
    match = re.search(r"\s*-\s*(\d+)\s*$", value)
    if match:
        return match.group(1)
    
    # Если дефиса нет, ищем просто цифры в конце
    match = re.search(r"(\d+)\s*$", value)
    if match:
        return match.group(1)
        
    return ""


def return_name_in_arr_vsemi(name: Any) -> str:
    """
    Возвращает название товара без цены.
    """
    value = str(name or "").strip()
    
    # Удаляем цену из конца строки
    # Сначала пробуем удалить с дефисом и пробелами
    cleaned = re.sub(r"\s*-\s*\d+\s*$", "", value).strip()
    
    # Если дефиса не было, удаляем просто число
    cleaned = re.sub(r"\s*\d+\s*$", "", cleaned).strip()
    
    return cleaned


def return_stock_price_vsemi(name: Any) -> str:
    """Возвращает цену."""
    return _get_price_vsemi(name)


def return_extra_price_vsemi(name: Any) -> Any:
    price = return_stock_price_vsemi(name)
    product_name = return_name_in_arr_vsemi(name)

    return price


def fix_name_vsemi(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("🎮", ""),
        ("R510 ", ""),
        ("R920 ", ""),
        ("R940 ", ""),
        ("mm", ""),
        ("Gift Set Vinca ", ""),
        ("GB", ""),
        ("13 Pro+", "13 Pro +"),
        ("14 Pro+", "14 Pro +"),
        ("(NFC)", ""),
        ("8/256G", "8/256"),
        ("12/256G", "12/256"),
        ("12/512G", "12/512"),
        ("Grey", "Gray"),
        ("grey", "gray"),
        ("Google Pixel", "Pixel"),
        ("5G Obsidian", "Obsidian"),
        ("Mi Pad", "Xiaomi Pad"),
        ("VR2", "vr 2"),
        ("Ocean Teal", "teal"),
        ("Dualsence", "Dualsense"),
    ]

    for old, new in replacements:
        value = value.replace(old, new)

    if "Poco" in value:
        value = value.replace("5G", "")

    return value


def normalize_vsemi_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()

    if not raw_value:
        return []

    # 1. Сначала очищаем название от цены
    clean_name = return_name_in_arr_vsemi(raw_value)
    
    # 2. Применяем фиксы имени к чистому названию
    name = fix_name_vsemi(clean_name)

    # 3. Получаем цену
    price = return_stock_price_vsemi(raw_value)

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]