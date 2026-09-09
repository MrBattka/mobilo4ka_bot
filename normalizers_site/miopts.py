import re
from typing import Any

FLAGS = (
    "🇯🇵", "🇮🇳", "🇪🇺", "🇦🇪", "🇧🇷", "🇻🇳", "🇰🇼", "🇺🇸",
    "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺", "🇨🇦", "🇨🇱",
    "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿", "🇰🇷", "🇬🇺",
)


def _clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).replace("-", " ").strip()


def _get_price_number(value: Any) -> int:
    text = _clean_text(value)

    # Цена после символа рубля
    match = re.search(r"₽\s*(\d[\d\s]*)", text)
    if match:
        return int(match.group(1).replace(" ", ""))

    # Или последнее числовое значение в строке
    numbers = re.findall(r"\b\d[\d\s]{2,}\b", text)
    if numbers:
        return int(numbers[-1].replace(" ", ""))

    return 0


def _get_flag(value: str) -> str:
    value = value.rstrip()

    for flag in FLAGS:
        if value.endswith(flag):
            return flag

    return ""


def return_name_in_arr_miopts(name: Any) -> str:
    """
    Возвращает название товара без цены, но с флагом (если он есть).
    """
    value = _clean_text(name)
    
    # 1. Извлекаем флаг, чтобы не удалять его при очистке цены
    flag = _get_flag(value)
    
    # Временное название без флага для обработки цены
    name_without_flag = value[:-len(flag)].rstrip() if flag else value

    # 2. Удаляем цену из названия без флага.
    # Паттерн объяснение:
    # \s+          - один или несколько пробелов перед ценой (если цена отделена пробелом)
    # (?=\s*$)     - проверяем, что цена находится в самом конце строки (перед возможными пробелами до конца)
    # Однако, проще удалить всё, что похоже на цену в конце.
    # Цена может быть: 15800₽, 15800 ₽, 15 800₽, 15 800
    # Мы ищем: последовательность цифр (возможно с пробелами внутри) и опциональный ₽ в конце строки.
    
    # Обновленная регулярка для удаления цены в конце строки:
    # r"\s+₽?\s*\d[\d\s]*\s*$" - старый вариант мог быть слабым, если цена слитна.
    # r"\s*\d[\d\s]*₽?\s*$" - удаляет пробелы перед ценой, само число (с пробелами) и опциональный ₽.
    
    # Более надежный паттерн:
    # Ищем опциональные пробелы, затем цифру, затем любые цифры/пробелы, затем опциональный ₽, затем конец строки.
    cleaned_name = re.sub(
        r"\s*\d[\d\s]*₽?\s*$", 
        "", 
        name_without_flag
    ).strip()

    # 3. Собираем обратно: Название + пробел + Флаг (если флаг был)
    result = cleaned_name
    if flag:
        result = f"{cleaned_name} {flag}".strip()

    return result


def return_stock_price_miopts(name: Any) -> int:
    return _get_price_number(name) + 400


def return_extra_price_miopts(name: Any) -> int:
    return _get_price_number(name) + 700


def fix_name_miopts(name: Any) -> str:
    value = re.sub(r"\s+", " ", str(name or ""))

    replacements = [
        ("🆕", ""),
        ("Xiaomi", "Mi"),
        ("iaomi Mi", "Mi"),
        ("Poco", "POCO"),
        ("GB", ""),
        ("S24FE", "S24 FE"),
        ("Note 13 Pro Plus", "Note 13 Pro +"),
        ("Note 14 Pro Plus", "Note 14 Pro +"),
        (" 1шт", ""),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    models_without_5g = (
        "M55 ", "A25 ", "A35 ", "A55 ", "A26 ", "A36 ",
        "A56 ", "A37 ", "A57 ", "S24 ", "S25 ", "Mi 1",
        "POCO", "X7 ",
    )

    if any(model in value for model in models_without_5g):
        value = value.replace("5G", "", 1)

    return re.sub(r"\s+", " ", value).strip()


def normalize_miopts_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    name = fix_name_miopts(return_name_in_arr_miopts(raw_value))

    if len(row) > 1 and row[1] not in ("", None):
        price = str(row[1]).strip()
    else:
        price = str(return_stock_price_miopts(raw_value))

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]