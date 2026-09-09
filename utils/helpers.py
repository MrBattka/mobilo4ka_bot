import re
from typing import Optional

import re

def custom_sort_key_redmi_note(item):
    name = item["name"].lower()
    name = re.sub(r'\bxiaomi\b', 'mi', name)  # нормализуем
    name = re.sub(r'sm-[a-z]\d+[a-z]?/[a-z][a-z]', '', name)
    name = re.sub(r'[🇦-🇿]+', '', name)
    name = re.sub(r'👉.*$', '', name)
    name = re.sub(r'\(.*не включается.*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'мятая коробка', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()

    if 'mi ' in name and 'note' not in name:
        series_match = re.search(r'mi\D*(\d+)', name)
        series = int(series_match.group(1)) if series_match else 0

        if 'ultra' in name:
            model_type = 4
        elif 'pro' in name and 't' in name:
            model_type = 3
        elif 't' in name:
            model_type = 2
        else:
            model_type = 1

        memory_match = re.search(r'(\d+)/(\d+)', name)
        ram = int(memory_match.group(1)) if memory_match else 0
        rom_str = memory_match.group(2) if memory_match else '0'
        rom = 1024 if 'tb' in rom_str.lower() else int(re.sub(r'\D', '', rom_str))
        is_5g = 1 if '5g' in name else 0

    # === Определяем категорию ===
    if 'mi ' in name and 'redmi' not in name and 'note' not in name:
        return _sort_key_mi(name)
    elif 'redmi' in name and 'note' not in name:
        return _sort_key_redmi(name)
    elif 'note' in name:
        return _sort_key_note(name)
    else:
        return (999, 0, 0, 0, 0, 0, 0)  # другие


def _sort_key_mi(name):
    series_match = re.search(r'mi\D*(\d+)', name)
    series = int(series_match.group(1)) if series_match else 0

    if 'ultra' in name:
        model_type = 4
    elif 'pro' in name and 't' in name:
        model_type = 3
    elif 't' in name:
        model_type = 2
    else:
        model_type = 1

    memory_match = re.search(r'(\d+)/(\d+)', name)
    ram = int(memory_match.group(1)) if memory_match else 0
    rom_str = memory_match.group(2) if memory_match else '0'
    rom_text = rom_str.lower()
    rom = 1024 if 'tb' in rom_text else int(re.sub(r'\D', '', rom_str))
    is_5g = 1 if '5g' in name else 0

    # 🔹 Отладка
    print(f"🔑 {name[:50]:<50} → series={series}, type={model_type}, 5G={is_5g}, ROM={rom}, RAM={ram}")

    return (1, series, model_type, -is_5g, rom, ram)


def _sort_key_redmi(name):
    # Ищем: redmi [a]?(\d+)([a-z]*)
    match = re.search(r'redmi\s+([a])?\s*(\d+)([a-z]*)', name, re.IGNORECASE)
    if match:
        is_a_series = match.group(1) is not None  # есть ли 'a' перед цифрой?
        series = int(match.group(2))
        suffix = match.group(3).lower()
    else:
        series = 0
        is_a_series = False
        suffix = ''

    # Определяем тип: A < обычные < C
    if is_a_series:
        sub_type = 1  # A-серия: Redmi A5, A7 и т.д.
    elif suffix == 'c':
        sub_type = 3  # C-серия
    else:
        sub_type = 2  # обычные Redmi (без A и C)

    memory_match = re.search(r'(\d+)/(\d+)', name)
    ram = int(memory_match.group(1)) if memory_match else 0
    rom_str = memory_match.group(2) if memory_match else '0'
    rom = int(re.sub(r'\D', '', rom_str)) if rom_str else 0
    is_5g = 1 if '5g' in name.lower() else 0

    return (
        2,              # группа: Redmi
        series,         # по возрастанию: A5=5, A7=7, 13, 15
        sub_type,       # A(1) → обычные(2) → C(3)
        -is_5g,         # 5G раньше 4G
        rom,
        ram,
        0
    )


def _sort_key_note(name):
    series_match = re.search(r'note (\d+)([a-z]*)', name, re.IGNORECASE)
    if series_match:
        series = int(series_match.group(1))
        suffix = series_match.group(2).lower()
    else:
        series = 0
        suffix = ''

    # Тип: base < s < Pro < Pro Plus
    name_lower = name.lower()
    if 'pro plus' in name_lower or re.search(r'pro.*plus|plus.*pro', name_lower):
        model_type = 4
    elif 'pro' in name_lower:
        model_type = 3
    elif suffix == 's':
        model_type = 2
    else:
        model_type = 1

    memory_match = re.search(r'(\d+)/(\d+)', name)
    ram = int(memory_match.group(1)) if memory_match else 0
    rom_str = memory_match.group(2) if memory_match else '0'
    rom_text = rom_str.lower()
    rom = 1024 if 'tb' in rom_text else int(re.sub(r'\D', '', rom_str))
    is_5g = 1 if '5g' in name_lower else 0

    return (
        3,          # группа: Note
        series,     # 13 → 14 → 15
        model_type, # base(1) → s(2) → pro(3) → pro plus(4)
        -is_5g,     # 5G раньше 4G
        rom,
        ram
    )
    
def custom_sort_key_galaxy_s(item):
    name = item["name"].lower()

    # Очистка
    name = re.sub(r'sm-[a-z]\d+[a-z]?/[a-z][a-z]', '', name)      # SM-S938B/DS
    name = re.sub(r'[🇦-🇿]+', '', name)                            # флаги
    name = re.sub(r'👉.*$', '', name)                             # скидки
    name = re.sub(r'\(.*не включается.*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'мятая коробка', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()

    # === Линейка: чтобы S шёл первым, потом Flip/Fold/Tab ===
    if 'z flip' in name or 'flip' in name:
        line = 'flip'
    elif 'z fold' in name or 'fold' in name:
        line = 'fold'
    elif 'galaxy s' in name or re.search(r'\bs\d{2}\b', name, re.IGNORECASE):
        line = 's'
    elif 'tab' in name:
        line = 'tab'
    else:
        line = 'other'

    # === Серия: S24, S25, S26 → цифры ===
    series_match = re.search(r'\b(?:galaxy\s+s|s|note|z\s*flip|z\s*fold|flip|fold)[-\s]*(\d{2})\b', name)
    series = int(series_match.group(1)) if series_match else 0

    # === Тип модели: порядок — base < FE < Edge < Plus < Ultra ===
    is_plus_like = '+' in name or 'plus' in name

    if 'ultra' in name:
        model_rank = 4
    elif is_plus_like:
        model_rank = 3
    elif 'edge' in name:
        model_rank = 2
    elif 'fe' in name:
        model_rank = 1
    else:
        model_rank = 0  # базовая модель

    # === Память: RAM и ROM (чем больше — тем позже) ===
    memory_match = re.search(r'(\d+)/(\d+)', name)
    ram = int(memory_match.group(1)) if memory_match else 0
    rom_str = memory_match.group(2) if memory_match else '0'
    rom_text = rom_str.lower()

    if 'tb' in rom_text:
        if '1' in rom_text:
            rom = 1024
        elif '2' in rom_text:
            rom = 2048
        else:
            rom = 0
    else:
        rom = int(re.sub(r'\D', '', rom_str))

    # === 5G — пусть будет после 4G (если важно) ===
    is_5g = 1 if '5g' in name else 0

    # Приоритет линеек (S → Z Flip → Z Fold → Tab)
    line_priority = {'s': 1, 'flip': 2, 'fold': 3, 'tab': 4, 'other': 5}

    return (
        line_priority[line],   # группа: S, Flip, Fold, Tab
        series,                # поколение: 24 → 25 → 26
        model_rank,            # тип: base(0) → FE(1) → Edge(2) → Plus(3) → Ultra(4)
        is_5g,                 # 4G → 5G
        rom,                   # ROM: 128 → 256 → 512 → 1Tb
        ram                    # RAM: 8 → 12 → 16
    )
    
def custom_sort_key_galaxy_a(item):
    name = item["name"].lower()

    # Очищаем от мусора
    name = re.sub(r'sm-[a-z]\d+[a-z]?/[a-z][a-z]', '', name)      # SM-A576B/DS
    name = re.sub(r'[🇦-🇿]+', '', name)                            # флаги
    name = re.sub(r'👉.*$', '', name)                             # скидки
    name = re.sub(r'\(.*не включается.*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'мятая коробка', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()

    # === Извлекаем номер модели: A17, A26, A35, A36, A37, A55, A56, A57 ===
    series_match = re.search(r'a(\d{2})', name)
    series = int(series_match.group(1)) if series_match else 0

    # === Память ===
    memory_match = re.search(r'(\d+)/(\d+)', name)
    ram = int(memory_match.group(1)) if memory_match else 0
    rom_str = memory_match.group(2) if memory_match else '0'
    rom = int(re.sub(r'\D', '', rom_str))

    # === 5G признак (если есть — пусть будет после 4G) ===
    is_5g = 1 if '5g' in name else 0

    return (
        series,     # A17=17, A26=26, ..., A57=57
        -is_5g,     # 5G после 4G
        rom,        # ROM: 128 → 256 → 512
        ram         # RAM: 6 → 8 → 12
    )

def additional_cost(price: float) -> float:
    if price < 50000:
        percent = 1
    else:
        percent = None
        
    if price < 50000:
        extra = (price / 100) * percent
    else:
        extra = 500

    import math
    extra_rounded = math.ceil(extra / 100) * 100
    
    return price + extra_rounded

def checkUsed(name):
        return (
        '"A-"' in name  or
        '"A"' in name or
        '"A+"' in name  or
        '"B-"' in name  or
        '"B"' in name or
        '"B+"' in name  or
        '"C-"' in name  or
        '"C"' in name or
        '"C+"' in name or
        '"А-"' in name  or
        '"А"' in name or
        '"А+"' in name  or
        '"В-"' in name  or
        '"В"' in name or
        '"В+"' in name  or
        '"С-"' in name  or
        '"С"' in name or
        '"С+"' in name 
    )

def is_flags_in_name(name: str, flags: list) -> str:
    has_flag = any(flag in name for flag in flags)
    return name if has_flag else f'{name} - '

def normalize_number(s: str) -> Optional[float]:
    s = re.sub(r'[^\d.,]', '', s.replace('\xa0', ''))
    s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return None
    
def is_item_allowed(name: str) -> bool:
    """
    Проверяет, разрешено ли добавлять позицию.
    Возвращает True, если товар прошёл все проверки.
    """
    if not name or len(name.strip()) < 3:
        return False
    name_lower = name.lower().strip()

    # 🔺 Запрещённые слова (полное совпадение или подстрока)
    banned_keywords = [
        'asis', 'обменка', 'пломба', 'inoi', 'right', 'left',
        'вилка', 'ссылка', 'минус', 'прайс', 'акция', 'скидка',
        'сегодня', 'поставка', 'в наличии', 'наличие', 'минимум',
        'упак', 'компл', 'партия', 'б/у', "актив", "нет серийн",
        "уценка", "дефект", "мятая", "не вкл"
    ]
    if any(kw in name_lower for kw in banned_keywords):
        print(f"🚫 Пропущено (ключевое слово): {name}")
        return False

    # 🔺 Пропускаем, если есть кавычки
    if '"' in name or '«' in name or '»' in name:
        print(f"🚫 Пропущено (кавычки): {name}")
        return False

    # 🔺 Пропускаем строки с подозрительными эмодзи
    forbidden_emojis = ['❤️', '🌟', '🔥', '🧧', '💡', '🔴', '🟠', '🟡', '⛄']
    if any(emoji in name for emoji in forbidden_emojis):
        print(f"🚫 Пропущено (эмодзи): {name}")
        return False

    # 🔺 Пропускаем, если выглядит как заголовок
    if any(name_lower.startswith(prefix) for prefix in ["от", "минимум", "скидка", "акция"]):
        print(f"🚫 Пропущено (начинается с): {name}")
        return False

    # 🔺 Пропускаем, если только цифры или слишком коротко
    cleaned = re.sub(r'[^\w]', '', name_lower)
    if len(cleaned) < 3:
        print(f"🚫 Пропущено (слишком коротко/цифры): {name}")
        return False

    return True
    
def postprocess_name(name: str) -> str:
    """
    Обрабатывает название перед выводом:
     - заменяет или удаляет бренды и маркеры
     - всегда возвращает читаемую строку
    """
    if not isinstance(name, str) or not name.strip():
        return name

    name = name.strip()

    replacements = [
        (r'\bSamsung Galaxy\b', ''),
        (r'\bApple\b', ''),
        (r'\bGARMIN\b', ''),
        (r'\bGarmin\b', ''),
        (r'Xiaomi 1', 'Mi 1'),
        (r'Xiaomi Pad', 'Mi Pad'),
        (r'Redmi Note', 'Note'),
        (r'\bXiaomi\b', ''),
        (r'\bGoogle\b', ''),
        (r'\bValve\b', ''),
        (r'\bSamsung\b', ''),
        (r'\bA17 4G\b', 'A17'),
        (r'\bA26 5G\b', 'A26'),
        (r'\bA36 5G\b', 'A36'),
        (r'\bA56 5G\b', 'A56'),
        (r'\bA57 5G\b', 'A57'),
        (r'\bA37 5G\b', 'A37'),
        (r'\bA55 5G\b', 'A55'),
        (r'\bA35 5G\b', 'A35'),
        (r'\bZ Flip6\b', 'Z Flip 6'),
        (r'\bZ Fold6\b', 'Z Fold 6'),
        (r'\bZ Flip7\b', 'Z Flip 7'), 
        (r'\bZ Fold7\b', 'Z Fold 7'),
        (r'\bXioami Pad\b', 'Mi Pad'),
        (r'\bGalaxy Tab\b', 'Tab'),
        (r'\bWatch7\b', 'Watch 7'),
        (r'\bWatch8\b', 'Watch 8'),
        (r'\bNord CE 6\b', 'Nord CE6'),
        (r'\bGalaxy S\b', 'S'),
        ('GB', '')
    ]

    for pattern, replacement in replacements:
        if replacement is None:
            replacement = ''
        name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)

    # Убираем лишние пробелы и символы
    name = re.sub(r'\s+', ' ', name).strip(' -.,')

    return name if name else "[товар]"
  
def _natural_key(text: str) -> list:
    """
    Преобразует строку в список для "естественнй" сортировки.
    Пример:
        "iPhone 10 Pro" → ['iphone ', 10, ' pro']
        "iPhone 9 Pro"  → ['iphone ', 9, ' pro']
    Теперь 10 > 9 → правильно!
    """
    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    return [convert(part) for part in re.split(r'(\d+)', text)]
    
def returnFlags(name):
    if 'RU/A' in name:
        return name.replace('RU/A', '🇷🇺')
    elif 'RU' in name:
        return name.replace('RU', '🇷🇺')
    elif 'LL/A' in name:
        return name.replace('LL/A', '🇺🇸')
    elif 'LW/A' in name:
        return name.replace('LW/A', '🇺🇸')
    elif 'EU' in name:
        return name.replace('EU', '🇪🇺')
    elif 'KZ' in name:
        return name.replace('KZ', '🇰🇿')
    elif 'AA/A' in name:
        return name.replace('AA/A', '🇦🇪')
    elif 'AA' in name:
        return name.replace('AA', '🇦🇪')
    elif 'AE/A' in name:
        return name.replace('AE/A', '🇦🇪')
    elif 'AE' in name:
        return name.replace('AE', '🇦🇪')
    elif 'CL/A' in name:
        return name.replace('CL/A', '🇨🇦')
    elif 'CL' in name:
        return name.replace('CL', '🇨🇱')
    elif 'AE/A' in name:
        return name.replace('AE/A', '🇦🇪')
    elif 'HN/A' in name:
        return name.replace('HN/A', '🇮🇳')
    elif 'HN' in name and 'MUHN2' not in name:
        return name.replace('HN', '🇮🇳')
    elif 'MY' in name and 'MYD' not in name:
        return name.replace('MY', '🇲🇾')
    elif 'CN' in name:
        return name.replace('CN', '🇨🇳')
    elif 'LZ/A' in name:
        return name.replace('LZ/A', '🇨🇱')
    elif 'LZ' in name:
        return name.replace('LZ', '🇨🇱')
    elif 'HK' in name:
        return name.replace('HK', '🇭🇰')
    elif 'VN' in name:
        return name.replace('VN', '🇻🇳')
    elif 'CH/A' in name:
        return name.replace('CH/A', '🇨🇳')
    elif 'CH' in name:
        return name.replace('CH', '🇨🇳')
    elif 'SA/A' in name:
        return name.replace('SA/A', '🇸🇦')
    elif 'SA' in name:
        return name.replace('SA', '🇸🇦')
    elif 'US' in name and 'USB-C' not in name:
        return name.replace('US', '🇺🇸')
    elif 'ZA/A' in name:
        return name.replace('ZA/A', '🇿🇦')
    elif 'ZA' in name:
        return name.replace('ZA', '🇿🇦')
    elif 'AFA' in name:
        return name.replace('AFA', '🇿🇦')
    elif 'AFR' in name:
        return name.replace('AFR', '🇿🇦')
    elif 'ZD/A' in name:
        return name.replace('ZD/A', '🇪🇺')
    elif 'ZD' in name:
        return name.replace('ZD', '🇪🇺')
    elif 'BA' in name:
        return name.replace('BA', '🇬🇧')
    elif 'GB' in name:
        return name.replace('GB', '🇬🇧')
    elif 'TH/A' in name:
        return name.replace('TH/A', '🇹🇭')
    elif 'J/A' in name:
        return name.replace('J/A', '🇯🇵')
    elif 'QL' in name:
        return name.replace('QL', '🇯🇵')
    elif 'UK' in name:
        return name.replace('UK', '🇬🇧')
    elif 'AF' in name:
        return name.replace('AF', '🇿🇦')
    elif 'IND' in name:
        return name.replace('IND', '🇮🇩')
    elif 'VCA' in name:
        return name.replace('VCA', '🇨🇦')
    elif 'XA' in name:
        return name.replace('XA', '🇦🇺')
    elif 'HU' in name:
        return name.replace('HU', '🇭🇺')
    elif 'HUA' in name:
        return name.replace('HUA', '🇭🇺')
    elif 'B/A' in name:
        return name.replace('B/A', '🇬🇧')
    elif 'ZDA' in name:
        return name.replace('ZDA', '🇪🇺')
    elif 'AH/A' in name:
        return name.replace('AH/A', '🇦🇪')
    elif 'AH' in name:
        return name.replace('AH', '🇦🇪')
    elif 'KG/A' in name:
        return name.replace('KG/A', '🇪🇺')
    elif 'AN/A' in name:
        return name.replace('AN/A', '🇯🇴')
    elif 'ZP/A' in name:
        return name.replace('ZP/A', '🇭🇰')
    elif 'TN/A' in name:
        return name.replace('TN/A', '🇻🇳')
    elif 'TW' in name:
        return name.replace('TW', '🇹🇼')
    elif 'TW/A' in name:
        return name.replace('TW/A', '🇹🇼')
    elif 'VC/A' in name:
        return name.replace('VC/A', '🇨🇦')
    elif 'HX/A' in name:
        return name.replace('HX/A', '🇦🇿')
    elif 'PY' in name:
        return name.replace('PY', '🇦🇪')
    elif 'JP' in name:
        return name.replace('JP', '🇯🇵')
    elif 'QN/A' in name:
        return name.replace('QN/A', '🇪🇺')
    elif 'SG' in name:
        return name.replace('SG', '🇸🇬')
    elif 'C/A' in name:
        return name.replace('C/A', '🇨🇦')
    elif 'CA' in name:
        return name.replace('CA', '🇨🇦')
    elif 'BE/A' in name:
        return name.replace('BE/A', '🇧🇷')
    elif 'IN' in name:
        return name.replace('IN', '🇮🇩')
    elif 'SX/A' in name:
        return name.replace('SX/A', '🇦🇺')
    else:
        return f'{name} - '
    
def returnFlagsForOrder(name):
    if 'RU/A' in name:
        return name.replace('RU/A', '🇷🇺')
    elif 'RU' in name:
        return name.replace('RU', '🇷🇺')
    elif 'LL/A' in name:
        return name.replace('LL/A', '🇺🇸')
    elif 'LW/A' in name:
        return name.replace('LW/A', '🇺🇸')
    elif 'EU' in name:
        return name.replace('EU', '🇪🇺')
    elif 'KZ' in name:
        return name.replace('KZ', '🇰🇿')
    elif 'AA/A' in name:
        return name.replace('AA/A', '🇦🇪')
    elif 'AA' in name:
        return name.replace('AA', '🇦🇪')
    elif 'AE/A' in name:
        return name.replace('AE/A', '🇦🇪')
    elif 'AE' in name:
        return name.replace('AE', '🇦🇪')
    elif 'CL/A' in name:
        return name.replace('CL/A', '🇨🇦')
    elif 'CL' in name:
        return name.replace('CL', '🇨🇱')
    elif 'AE/A' in name:
        return name.replace('AE/A', '🇦🇪')
    elif 'HN/A' in name:
        return name.replace('HN/A', '🇮🇳')
    elif 'HN' in name and 'MUHN2' not in name:
        return name.replace('HN', '🇮🇳')
    elif 'MY' in name and 'MYD' not in name:
        return name.replace('MY', '🇲🇾')
    elif 'CN' in name:
        return name.replace('CN', '🇨🇳')
    elif 'LZ/A' in name:
        return name.replace('LZ/A', '🇨🇱')
    elif 'LZ' in name:
        return name.replace('LZ', '🇨🇱')
    elif 'HK' in name:
        return name.replace('HK', '🇭🇰')
    elif 'VN' in name:
        return name.replace('VN', '🇻🇳')
    elif 'CH/A' in name:
        return name.replace('CH/A', '🇨🇳')
    elif 'CH' in name:
        return name.replace('CH', '🇨🇳')
    elif 'SA' in name:
        return name.replace('SA', '🇸🇦')
    elif 'US' in name and 'USB-C' not in name:
        return name.replace('US', '🇺🇸')
    elif 'ZA/A' in name:
        return name.replace('ZA/A', '🇿🇦')
    elif 'ZA' in name:
        return name.replace('ZA', '🇿🇦')
    elif 'AFA' in name:
        return name.replace('AFA', '🇿🇦')
    elif 'AFR' in name:
        return name.replace('AFR', '🇿🇦')
    elif 'ZD/A' in name:
        return name.replace('ZD/A', '🇪🇺')
    elif 'ZD' in name:
        return name.replace('ZD', '🇪🇺')
    elif 'BA' in name:
        return name.replace('BA', '🇬🇧')
    elif 'GB' in name:
        return name.replace('GB', '🇬🇧')
    elif 'TH/A' in name:
        return name.replace('TH/A', '🇹🇭')
    elif 'J/A' in name:
        return name.replace('J/A', '🇯🇵')
    elif 'QL' in name:
        return name.replace('QL', '🇯🇵')
    elif 'UK' in name:
        return name.replace('UK', '🇬🇧')
    elif 'AF' in name:
        return name.replace('AF', '🇿🇦')
    elif 'IND' in name:
        return name.replace('IND', '🇮🇩')
    elif 'VCA' in name:
        return name.replace('VCA', '🇨🇦')
    elif 'XA' in name:
        return name.replace('XA', '🇦🇺')
    elif 'HU' in name:
        return name.replace('HU', '🇭🇺')
    elif 'HUA' in name:
        return name.replace('HUA', '🇭🇺')
    elif 'B/A' in name:
        return name.replace('B/A', '🇬🇧')
    elif 'ZDA' in name:
        return name.replace('ZDA', '🇪🇺')
    elif 'AH/A' in name:
        return name.replace('AH/A', '🇦🇪')
    elif 'AH' in name:
        return name.replace('AH', '🇦🇪')
    elif 'KG/A' in name:
        return name.replace('KG/A', '🇪🇺')
    elif 'AN/A' in name:
        return name.replace('AN/A', '🇯🇴')
    elif 'ZP/A' in name:
        return name.replace('ZP/A', '🇭🇰')
    elif 'TN/A' in name:
        return name.replace('TN/A', '🇻🇳')
    elif 'TW' in name:
        return name.replace('TW', '🇹🇼')
    elif 'TW/A' in name:
        return name.replace('TW/A', '🇹🇼')
    elif 'VC/A' in name:
        return name.replace('VC/A', '🇨🇦')
    elif 'HX/A' in name:
        return name.replace('HX/A', '🇦🇿')
    elif 'PY' in name:
        return name.replace('PY', '🇦🇪')
    elif 'JP' in name:
        return name.replace('JP', '🇯🇵')
    elif 'QN/A' in name:
        return name.replace('QN/A', '🇪🇺')
    elif 'SG' in name:
        return name.replace('SG', '🇸🇬')
    elif 'C/A' in name:
        return name.replace('C/A', '🇨🇦')
    elif 'CA' in name:
        return name.replace('CA', '🇨🇦')
    elif 'BE/A' in name:
        return name.replace('BE/A', '🇧🇷')
    elif 'IN' in name:
        return name.replace('IN', '🇮🇩')
    elif 'SX/A' in name:
        return name.replace('SX/A', '🇦🇺')
    else:
        return name