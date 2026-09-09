from typing import List, Dict, Any, Optional
import gspread
import asyncio
import re
import json

from config.settings import (DATA_DIR, SELECTED_FILES, 
                             SECTION_HEADERS, SHEETS_ID_FOR_ORDER,
                             CREDENTIALS_FILE)
from returnNameWithID import match_product
from defaultFixName import default_fix_name
from utils.helpers import (
    additional_cost, is_flags_in_name, normalize_number, postprocess_name,
    _natural_key, is_item_allowed
    )

from utils.helpers import returnFlagsForOrder, returnFlags

# Загрузка флагов (можно вынести в settings)
flagsArr = [
    '🇷🇺', '🇺🇸', '🇪🇺', '🇰🇿', '🇦🇪', '🇨🇦', '🇨🇱', '🇮🇳', '🇲🇾', '🇨🇳',
    '🇭🇰', '🇻🇳', '🇸🇦', '🇿🇦', '🇬🇧', '🇹🇭', '🇯🇵', '🇮🇩', '🇦🇺', '🇭🇺',
    '🇯🇴', '🇹🇼', '🇦🇿', '🇸🇬', '🇧🇷', '🇰🇷', '🇵🇭', '🇲🇽', '🇳🇱', '🇩🇪', '🇫🇷', '🇮🇹', '🇪🇸'
]

TRANSPORT_EMOJI = {
    '🛰', '🛩', '🚀', '🚁', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚉', '🚊',
    '🚝', '🚞', '🚋', '🚌', '🚍', '🚎', '🚐', '🚗', '🚕', '🚙', '🛻', '🚚',
    '🚛', '🚜', '🏎', '🏍', '🛵', '🦽', '🦼', '🛹', '🛼', '🚲', '🛴', 'BMX'
}

# === Загрузка данных из JSON ===
loaded_data = {}

for filename in SELECTED_FILES:
    file_path = DATA_DIR / filename
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_data[filename] = json.load(f)
                print(f"✅ Загружено: {filename}")
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка чтения {filename}: {e}")
    else:
        print(f"❗ Файл не найден: {file_path}")

# === Обработка строк ===
async def load_name_used_from_sheet():
    try:
        name_list, used_list = await asyncio.to_thread(
            fetch_name_used_from_fifth_sheet,
            SHEETS_ID_FOR_ORDER,
            CREDENTIALS_FILE
        )
        return name_list, used_list
    except Exception as e:
        print(f"❌ Ошибка загрузки с Google Sheets: {e}")
        return [], []

async def get_fresh_name_used_lists() -> tuple[list[str], list[str]]:
    try:
        name_list, used_list = await asyncio.to_thread(
            fetch_name_used_from_fifth_sheet,
            SHEETS_ID_FOR_ORDER,
            CREDENTIALS_FILE
        )
        # Убираем дубликаты, сохраняя порядок
        name_list = list(dict.fromkeys(name_list))
        used_list = list(dict.fromkeys(used_list))
        return name_list, used_list
    except Exception as e:
        print(f"❌ Ошибка загрузки с Google Sheets: {e}")
        return [], []
    
def _extract_name_and_price_hi(text: str) -> Optional[Dict[str, Any]]:
    """
    Извлекает название и цену, только если цена идёт после `-`
    Сохраняет флаги (эмодзи) в названии.
    """
    if not text:
        return None

    text = re.sub(r'\[.*?HiCatalog\s*Bot:\s*', '', text, flags=re.IGNORECASE)

    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text.strip())
    if not text:
        return None

    # Пропускаем строки, похожие на заголовки или мусор
    if any(kw in text.lower() for kw in ["прайс", "актуально", "от", "шт", "итого", "сумма", "всего"]):
        return None
    if text.startswith(("от", "минимум", "скидка", "🌟", "🔴", "🟠", "🟡", "💡", "❤️")):
        return None
    

    # 🔍 Ищем цену: - 129500
    price_match = re.search(
        r'''
        -                           # обязательный дефис
        \s*                         # пробелы после
        (?P<price>\d{4,6})          # цена: 4–6 цифр
        \s*                         # пробелы
        (?:₽|р\.?|руб\.?|RUB)?      # опционально валюта
        \s*                         # пробелы
        [^\d\w₽рРуб\.]*             # разрешаем эмодзи и символы после
        $                           # до конца строки
        ''',
        text,
        re.IGNORECASE | re.VERBOSE
    )

    if not price_match:
        print(f"❌ Нет цены после '-': {text}")
        return None

    raw_price = price_match.group("price")
    price_start, price_end = price_match.span()

    try:
        price_val = int(raw_price)
    except:
        print(f"❌ Не число: {raw_price}")
        return None

    # Название — всё до `-`
    name_part = text[:price_start].strip()

    # 🔥 ИЗВЛЕКАЕМ ФЛАГИ ДО ОЧИСТКИ
    flag_pattern = r"[\U0001F1E6-\U0001F1FF]{2}"  # Региональные флаги
    flags = "".join(re.findall(flag_pattern, name_part))

    # Очищаем название: УДАЛЯЕМ МУСОР, но НЕ УДАЛЯЕМ ЭМОДЗИ
    name = re.sub(r'^[\-\:\.\s]+', '', name_part)
    name = re.sub(r'\s+', ' ', name).strip()

    # Удаляем транспортные эмодзи
    for emoji in TRANSPORT_EMOJI:
        name = name.replace(emoji, '')

    # Удаляем ненужные слова
    name = re.sub(r'\b(шт|шт\.|уп|упак|упак\.|компл|партия|от)\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()

    # 🔴 ЗАМЕНЯЕМ ПРОБЛЕМНУЮ СТРОКУ:
    # БЫЛО: name = re.sub(r'[^\w\s\-\(\)/\.\+]', '', name, flags=re.UNICODE)  # ❌ УДАЛЯЕТ ФЛАГИ
    # СТАЛО: удаляем ТОЛЬКО нежелательные символы, НО оставляем эмодзи и флаги
    name = re.sub(r'[^\w\s\-\(\)/\.\+\U0001F1E6-\U0001F1FF]', '', name, flags=re.UNICODE)
    name = re.sub(r'\s+', ' ', name).strip()

    # Удаляем флаги из текста, чтобы не дублировались
    name = re.sub(flag_pattern, '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    # 🔥 Возвращаем флаги в конец
    if flags:
        name = f"{name} {flags}".strip()

    if not name or len(name) < 5:
        print(f"❌ Имя слишком короткое: '{name}'")
        return None

    return {
        "name": name,
        "price": additional_cost(price_val)
    }

def _extract_name_and_price_dyson(text: str) -> Optional[Dict[str, Any]]:
    """
    Извлекает название и цену из строки.
    Добавляет [без кейса], [с кейсом], [с дорожным чехлом] перед флагом.
    Флаг — всегда в конце.
    """
    if not text:
        return None
    
    text = re.sub(r'\[.*?VOSH🔅D:\s*', '', text, flags=re.IGNORECASE)
    
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text.strip())
    if not text:
        return None

    # Пропускаем мусор
    skip_keywords = [
        "актуально", "💡", "от", "шт", "ссылка", "вилка", "минус", "прайс", "сегодня", "поставка",
        "🚗", "❤️", "🟠", "🔴", "🟡", "⛄🔗", "🌟", "минимум", "скидка"
    ]
    if any(kw in text.lower() for kw in skip_keywords):
        return None
    if text.startswith(("от", "минимум", "скидка", "❤️", "🚗", "🟠", "🔴", "🟡")):
        return None

    # 🔍 Ищем цену: 5–6 цифр после `-` или без, до [ или конца
    price_match = re.search(
        r'-?\s*(?P<price>\d{5,6})\s*(?:₽|р\.?|руб\.?|RUB)?\s*(?=\s*\[|$)',
        text,
        re.IGNORECASE
    )
    if not price_match:
        print(f"❌ Нет пятизначной цены: {text}")
        return None

    raw_price = price_match.group("price")
    price_start, price_end = price_match.span()

    try:
        price_val = int(raw_price)
    except:
        print(f"❌ Не число: {raw_price}")
        return None

    # Всё до цены
    name_part = text[:price_start].strip()
    name_part = re.sub(r'\s+', ' ', name_part).strip(' -.,')

    # Извлекаем флаг из начала или конца
    flag_match = re.search(r'([🇦-🇿]{1,4})', name_part)
    flag = flag_match.group(1) if flag_match else ''
    # Удаляем флаг из name_part
    name_clean = re.sub(r'[🇦-🇿]{1,4}', '', name_part).strip()
    # Очищаем от лишних символов
    name_clean = re.sub(r'\s+', ' ', name_clean).strip(' -.,')

    # Удаляем скобки с комментариями — они будут добавлены позже
    name_clean = re.sub(r'\([^)]*?\)', '', name_clean).strip()
    # Удаляем ссылки
    name_clean = re.sub(r'\bhttps?://\S+', '', name_clean).strip()
    name_clean = re.sub(r'\s+', ' ', name_clean).strip()

    # 🔥 Добавляем комментарии сразу после названия, но ДО флага
    comment_parts = []
    # if "[без кейса]" in text:
    #     comment_parts.append("[без кейса]")
    # if "[с кейсом]" in text:
    #     comment_parts.append("[с кейсом]")
    # if "[с дорожным чехлом]" in text:
    #     comment_parts.append("[с дорожным чехлом]")

    # Собираем: название + комментарии + флаг
    final_name = name_clean
    if comment_parts:
        final_name += " " + " ".join(comment_parts)
    if flag:
        final_name += " " + flag

    final_name = re.sub(r'\s+', ' ', final_name).strip()
    final_name = final_name.replace("📷", "")

    return {
        "name": final_name,
        "price": additional_cost(price_val)
    }
    
    
    
    
    # split_bracket = re.sub(r'\([^)]*?\)', '', name_clean)

def _extract_name_and_price_garmin(text: str) -> Optional[Dict[str, Any]]:
    """
    Парсит строку с шестого листа:
    - Извлекает флаги (эмодзи) и перемещает их в конец названия
    - Находит цену: всё, что слитно перед ₽ (до пробела/тире)
    - Вставляет ' - ' перед ценой, если его нет
    - Возвращает название (с флагами в конце) и цену
    """
    if not text:
        return None
    
    text = re.sub(r'\[.*?ru:\s*', '', text, flags=re.IGNORECASE)

    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text.strip())
    if not text:
        return None

    # Пропускаем заголовки
    skip_keywords = ["в наличии", "новое поступление", "гарантия", "цена", "актуально"]
    if any(kw in text.lower() for kw in skip_keywords):
        return None

    # 🔍 Ищем флаги ДО обработки
    flag_pattern = r'[\U0001F1E6-\U0001F1FF]{2}'
    flags = ''.join(re.findall(flag_pattern, text))

    # Удаляем флаги из текста
    text_no_flags = re.sub(flag_pattern, '', text)
    text_no_flags = re.sub(r'\s+', ' ', text_no_flags).strip()

    # 🔍 Ищем ₽
    currency_match = re.search(r'₽', text_no_flags)
    if not currency_match:
        print(f"❌ Нет символа ₽: {text}")
        return None

    currency_pos = currency_match.start()

    # Шаг 1: Находим начало цены — идём назад, пока цифры, точки или запятые
    price_end = currency_pos
    price_start = price_end
    while price_start > 0 and text_no_flags[price_start - 1] in '0123456789.,':
        price_start -= 1

    if price_start == price_end:
        print(f"❌ Не найдено число перед ₽: {text_no_flags}")
        return None

    raw_price = text_no_flags[price_start:price_end].strip()
    cleaned_price = re.sub(r'[.,]', '', raw_price)  # убираем разделители

    if not cleaned_price.isdigit():
        print(f"❌ Цена не число: {raw_price} из {text_no_flags}")
        return None

    try:
        price_val = int(cleaned_price)
    except:
        print(f"❌ Ошибка парсинга цены: {cleaned_price}")
        return None

    # Шаг 2: Часть ДО цены
    before_price_text = text_no_flags[:price_start].strip()

    # Проверяем, заканчивается ли на тире (с пробелами)
    if re.search(r'[-—–]\s*$', before_price_text):
        name_part = re.sub(r'[-—–]\s*$', '', before_price_text).strip()
    else:
        name_part = before_price_text

    # Удаляем 'GARMIN' (по желанию)
    name_clean = re.sub(r'\bGarmin\b', '', name_part, flags=re.IGNORECASE)
    name_clean = re.sub(r'\s+', ' ', name_clean).strip(' -.,')

    # ✅ Формируем имя: сначала название, потом тире, и в конце — флаги
    # final_name = f"{name_clean} -"
    if flags:
        name_clean += f" {flags}"

    return {
        "name": name_clean,
        "price": additional_cost(price_val) + 1000
    }

def _extract_name_and_price_opt(row: List[str]) -> Optional[Dict[str, Any]]:
    """
    Извлекает название и цену с 5-го листа.
    - Сначала заменяет текстовые флаги на эмодзи с помощью returnFlags
    - Пропускает строки с запрещёнными словами, кавычками и ошибками
    - Возвращает оригинальное (очищенное) название
    """
    if len(row) < 7:
        return None

    # Берём название как есть
    serial_num = row[6].strip()
    name = row[2].strip()
    price_str = row[6].strip()

    # 🔁 ПЕРВОЕ, ЧТО ДЕЛАЕМ — ЗАМЕНЯЕМ ФЛАГИ
    name = returnFlagsForOrder(name)

    # Проверки на пустоту
    if not name or not price_str:
        return None

    # 🔺 Пропускаем, если есть запрещённые слова
    banned_words = ['Right', 'Left', 'обменка', 'ASIS', 'пломба']
    for word in banned_words:
        if re.search(rf'\b{re.escape(word)}\b', name, re.IGNORECASE):
            print(f"🚫 Пропущено (запрещённое слово): {name} → содержит '{word}'")
            return None

    # 🔺 Пропускаем, если есть кавычки
    if '"' in name:
        print(f"🚫 Пропущено (кавычки): {name}")
        return None

    # 🔺 Пропускаем, если ошибка в цене
    if '#ERROR' in price_str:
        print(f"🚫 Пропущено (ошибка в цене): {name}")
        return None

    # Очистка и парсинг цены
    price_clean = re.sub(r'[^\d]', '', price_str)
    if not price_clean.isdigit():
        print(f"🚫 Некорректная цена: {price_str} для {name}")
        return None

    try:
        price_val = int(price_clean)
    except ValueError:
        return None

    # ✅ Возвращаем название с ЭМОДЗИ-флагами и оригинальным содержанием
    return {
        "name": name,
        "price": price_val,
        "serial_num": serial_num
    }

def _extract_name_and_price_miopts_sheet(lines: List[str], idx: int) -> Optional[Dict[str, Any]]:
    if idx >= len(lines):
        return None

    current_line = lines[idx].strip()

    # 🔴 ИГНОРИРУЕМ строки с "Inoi"
    if "Inoi" in current_line or "inoi" in current_line.lower():
        print(f"🚫 Пропущено (Inoi): {current_line}")
        return None

    next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""

    # Очищаем название: удаляем [что-то]MiOptMos: включая сам флаг
    clean_current_line = re.sub(r'\[.*?MiOptMos:\s*', '', current_line, flags=re.DOTALL).strip()
    # Также очищаем от "от 3 шт." если осталось
    clean_current_line = re.sub(r'\s*\(?\s*от\s+3\s*шт\.\)?', '', clean_current_line, flags=re.IGNORECASE).strip()

    # === Вариант 1: цена в той же строке ===
    price_match_inline = re.search(r'(\d{4,6})₽([\🇦-🇿]{2})?$', current_line)
    if price_match_inline:
        raw_price = price_match_inline.group(1)
        flag = price_match_inline.group(2) or ''
        name_part = clean_current_line[:price_match_inline.start()].strip()

        try:
            base_price = int(raw_price)
        except ValueError:
            return None

        final_price = additional_cost(base_price) + 700
        final_price_min = final_price - 300  # ВСЕГДА для 3-го листа

        name = f"{name_part}{f' {flag}' if flag else ''}".strip()
        return {
            "name": name,
            "price": final_price,
            "price_min": final_price_min
        }

    # === Вариант 2: цена в следующей строке ===
    price_match_next = re.search(r'^(\d{4,6})₽([\🇦-🇿]{2})?$', next_line)
    if price_match_next:
        raw_price = price_match_next.group(1)
        flag = price_match_next.group(2) or ''
        name_part = clean_current_line

        try:
            base_price = int(raw_price)
        except ValueError:
            return None

        final_price = additional_cost(base_price) + 700
        final_price_min = final_price - 300
        name = f"{name_part}{f' {flag}' if flag else ''}".strip()
        
        return {
            "name": name,
            "price": final_price,
            "price_min": final_price_min
        }

    return None

def _extract_name_and_price_seventh_sheet(lines: List[str], idx: int) -> Optional[Dict[str, Any]]:
    """
    Обрабатывает 7-й лист:
    - Текущая строка: название + цена через '-'
    - Следующая строка: артикул (например, '010-13123-00' или 'Артикул: 010-13123-00')
    - Добавляет артикул в название: (арт: XXX)
    """
    if idx >= len(lines):
        return None

    current_line = lines[idx].strip()
    next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""

    # Пропускаем разделители и пустые строки
    if re.match(r'^[-—]{10,}$', current_line) or not current_line:
        return None

    # Ищем цену: после `-` и до конца/₽
    price_match = re.search(
        r'-\s*(?P<price>\d[\d\s]{3,5}\d)\s*(?:₽|р\.?|руб\.?|RUB)?\s*$',
        current_line,
        re.IGNORECASE
    )
    if not price_match:
        print(f"❌ Нет цены: {current_line}")
        return None

    raw_price = price_match.group("price")
    price_val_str = re.sub(r'[^\d]', '', raw_price)
    try:
        price_val = int(price_val_str)
    except ValueError:
        print(f"❌ Не число: {raw_price}")
        return None

    # Извлекаем основное название (до "-")
    name_part = current_line[:price_match.start()].strip()

    # Чистим от лишних символов (например, эмодзи ⌚️)
    name_part = re.sub(r'^[⌚️🔧📦💡❤️🌟\s]+', '', name_part).strip()

    # === Извлечение артикула из следующей строки ===
    part_number = ""

    if next_line:
        # Убираем "Артикул:", "Part Number:", etc.
        cleaned_next = re.sub(r'^[Аа]ртикул[:\s]*|[Pp]art[:\s]*[Nn]umber[:\s]*[:\-]?\s*', '', next_line).strip()
        # Ищем сам артикул: формат 010-XXXXX-XX
        pn_match = re.search(r'\b\d{3}-\d{5}-\d{2}[A-Z]?\b', cleaned_next)
        if pn_match:
            part_number = f" (арт: {pn_match.group(0)})"

    # Формируем финальное имя
    final_name = f"{name_part}{part_number}".strip()

    return {
        "name": final_name,
        "price": additional_cost(price_val)
    }


# === Форматирование ===
def format_section(emoji: str, model_name: str, items: List[Dict[str, Any]]) -> str:
    if not items:
        return ""
    if model_name:
        return f"{emoji} {model_name}\n{processed_list_to_text(items)}\n\n"
    else:
        return f"{processed_list_to_text(items)}\n\n"

def processed_list_to_text(items: List[Dict[str, Any]]) -> str:
    lines = []
    for it in items:
        price = it.get("price")
        price_min = it.get("price_min")

        # Форматируем цену
        if price_min and price_min < price:
            price_str = f"{int(price)} 👉 ({int(price_min)} - от 3шт.)"
        else:
            price_str = str(int(price))

        cleaned_name = postprocess_name(it["name"])
        cleaned_name = is_flags_in_name(cleaned_name, flagsArr)

        lines.append(f"<code> • {cleaned_name} {price_str}</code>")
    return "\n".join(lines)

# === Обработка листов ===
def fetch_name_used_from_fifth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> tuple[list, list]:
    import gspread
    from utils.helpers import returnFlagsForOrder

    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    ws = sh.worksheets()[4]  # пятый лист

    all_values = ws.get_all_values()
    name_list = []
    used_list = []

    for idx, row in enumerate(all_values):
        # Убедимся, что строка содержит достаточно столбцов
        if len(row) < 7:
            continue  # нужно минимум 7 столбцов (A-G)

        flag_cell = row[2].strip() if len(row) > 2 else ""       # C — флаг
        name_cell = row[6].strip() if len(row) > 6 else ""       # G — Наименование + Цена
        imei_cell = row[0].strip() if len(row) > 0 else ""       # A — IMEI (только для used)

        # Пропускаем заголовок и "Опт"
        if not name_cell or name_cell == "Наименование":
            continue
        if idx > 0 and len(row) > 6 and row[6] == "Опт":  # цена в G — это "Опт"?
            continue

        # Добавляем флаги к названию
        flagged_country = returnFlags(flag_cell)

        # Формируем итоговое имя: флаг + название
        full_name = f"{flagged_country}{name_cell}"

        # ❗️ВАЖНО: price здесь — это НЕ отдельная ячейка, а часть `name_cell`
        # Если в G6 у вас уже написано: "iPhone 15 Pro Max 200000", то так и оставляем
        # То есть мы НЕ выделяем цену отдельно — она уже в строке

        name_list.append(full_name)
        used_list.append(f"{full_name} imei{imei_cell}")

    return name_list, used_list

def process_first_sheet(ws, all_product_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()

    print(f"📊 Обработка первого листа: {len(all_values)} строк")

    # Если база ID не передана — собираем из loaded_data
    if all_product_data is None:
        all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}

    seen_product_ids: set = set()

    for row in all_values:
        if not row or not row[0]:
            continue

        extracted = _extract_name_and_price_hi(row[0])
        if not extracted:
            print(f"❌ Пропущено: {row[0]}")
            continue

        name = extracted["name"]

        # 🔽 ФИЛЬТР: проверяем до добавления
        if not is_item_allowed(name):
            print(f"❌ Отфильтровано (1 лист): {name}")
            continue

        # Пробуем привязать product_id — и если привязано, проверяем дубли по id
        to_default_name = default_fix_name(name)
        product_id = match_product(to_default_name, all_product_data) if to_default_name else None
        if product_id:
            if product_id in seen_product_ids:
                print(f"🔁 Пропущено (дубль по ID {product_id}): {name}")
                continue
            extracted["product_id"] = product_id
            seen_product_ids.add(product_id)
            print(f"✅ Добавлено с ID {product_id}: {name} → {extracted['price']}")
        else:
            # Если нет привязки — добавляем как раньше
            print(f"✅ Добавлено (без ID): {name} → {extracted['price']}")

        items.append(extracted)

    print(f"📦 Возвращено позиций с 1 листа: {len(items)}")
    return items

def process_third_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()
    lines = [row[0].strip() for row in all_values if row and row[0].strip()]

    print(f"📊 Обработка третьего листа: {len(lines)} строк")

    i = 0
    while i < len(lines):
        line = lines[i]
        extracted = _extract_name_and_price_miopts_sheet(lines, i)

        if extracted:
            items.append(extracted)
            print(f"✅ Добавлено: {extracted['name']} → {extracted['price']}")
            # Если использовали две строки (название + цена), пропускаем следующую
            if re.match(r'^\d{4,6}₽', lines[i + 1]) if i + 1 < len(lines) else False:
                i += 1
        else:
            print(f"❌ Пропущено: {line}")

        i += 1

    print(f"📦 Возвращено позиций (3 лист): {len(items)}")
    return items

def process_fourth_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()
    all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}
    print(f"📊 Всего ID в базе: {len(all_product_data)}")

    for row in all_values:
        if len(row) < 2:
            continue
        name, price_str = row[0].strip(), row[1].strip()
        if not name or not price_str or name.upper() in SECTION_HEADERS:
            continue
        if not is_item_allowed(name):
           print(f"❌ Отфильтровано (4 лист): {name}")
           continue

        price_val = normalize_number(price_str)
        if price_val is None:
            print(f"❌ Не распознана цена: {price_str} для {name}")
            continue

        cleaned_name = re.sub(r'\b(шт|шт\.|уп|упак|упак\.|кг|г|л|мл|компл|партия|от)\b', '', name, flags=re.IGNORECASE)
        cleaned_name = re.sub(r'[^\w\s\-\(\),./\s🇦-🇿]', '', cleaned_name, flags=re.UNICODE)
        cleaned_name = re.sub(r'\s{2,}', ' ', cleaned_name).strip(' -.,')
        cleaned_name = cleaned_name.replace("16Е", "16e").replace("16е", "16e")

        if not cleaned_name:
            continue

        item = {
            "name": cleaned_name,
            "price": additional_cost(price_val)
        }
        to_default_name = default_fix_name(cleaned_name)
        product_id = match_product(to_default_name, all_product_data)
        if product_id:
            item["product_id"] = product_id
            items.append(item)
            print(f"✅ ID {product_id}: {to_default_name}")
        else:
            print(f"❌ Нет ID: {to_default_name}")

    print(f"📦 Возвращено позиций с ID (4 лист): {len(items)}")
    return items

def process_fifth_sheet(ws, all_product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Обрабатывает 5-й лист:
    - Извлекает название и цену
    - Убирает дубликаты
    - Ищет product_id, используя нормализованное имя
    - Возвращает товары с оригинальным регистром названия
    """
    items = []
    seen_names = set()
    all_values = ws.get_all_values()

    print(f"📊 Обработка пятого листа: {len(all_values)} строк")

    for idx, row in enumerate(all_values):
        if not row or len(row) < 3:
            continue

        # Пропускаем заголовок
        if idx == 0 or row[2].strip() == "Наименование":
            continue

        # Извлекаем данные
        extracted = _extract_name_and_price_opt(row)
        if not extracted:
            continue

        # ✅ Сохраняем оригинальное название (с регистром!)
        original_name = extracted["name"]

        # Убираем дубликаты по оригинальному имени
        if original_name in seen_names:
            print(f"🔁 Пропущено (дубль): {original_name}")
            continue
        seen_names.add(original_name)

        # 🔎 Для поиска ID — используем нормализованное имя (в нижнем регистре)
        normalized_name = default_fix_name(original_name)
        # product_id = match_product(normalized_name, all_product_data)

        if not normalized_name:
            print(f"❌ Нет ID: {normalized_name}")
            continue

        # ✅ Формируем результат с ОРИГИНАЛЬНЫМ названием
        item = {
            "name": original_name,           # ← сохраняем как в таблице
            "price": extracted["price"],
            "product_id": normalized_name
        }
        items.append(item)
        print(f"✅ ID {normalized_name}: {original_name}")

    print(f"📦 Возвращено позиций с ID (5 лист): {len(items)}")
    return items

def process_sixth_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()

    print(f"📊 Обработка шестого листа: {len(all_values)} строк")

    for idx, row in enumerate(all_values):
        if not row or not row[0].strip():
            continue

        text = row[0].strip()
        print(f"🔍 [6 лист] Строка {idx}: {text}")

        extracted = _extract_name_and_price_garmin(text)
        if extracted:
            items.append(extracted)
            print(f"✅ Добавлено: {extracted['name']} → {extracted['price']}")
        else:
            print(f"❌ Пропущено: {text}")

    print(f"📦 Возвращено позиций (6 лист): {len(items)}")
    return items


def process_eighth_sheet(ws) -> List[Dict[str, Any]]:
    """
    Обрабатывает 8-й лист:
    - Берёт значение из колонки C (Модификация) как название
    - Берёт цену из колонки G (Цена за штуку)
    - Фильтрует по запрещённым словам ДО добавления
    """
    items = []
    all_values = ws.get_all_values()

    print(f"📊 Обработка восьмого листа: {len(all_values)} строк")

    for idx, row in enumerate(all_values):
        # Пропускаем заголовок и короткие строки
        if idx == 0 or len(row) < 7:
            continue

        modification = row[2].strip() if len(row) > 2 else ""   # Колонка C
        price_str = row[5].strip() if len(row) > 5 else ""      # Колонка G — Цена за штуку

        if not modification or not price_str or price_str == "Цена за штуку":
            continue

        # Очистка цены
        price_clean = re.sub(r'[^\d]', '', price_str)
        if not price_clean.isdigit():
            print(f"❌ Некорректная цена: {price_str} для {modification}")
            continue

        try:
            price_val = int(price_clean)
        except ValueError:
            continue

        # Формируем имя
        cleaned_name = re.sub(r'\s+', ' ', modification).strip()
        cleaned_name = re.sub(r'\b(в\s*наличии|акция|скидка)\b', '', cleaned_name, flags=re.IGNORECASE)
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()

        # Добавляем флаги
        name_with_flags = returnFlags(cleaned_name)

        if not name_with_flags or name_with_flags.strip() == "- ":
            continue

        # 🔽 ФИЛЬТР: проверяем до добавления
        if not is_item_allowed(name_with_flags):
            print(f"❌ Отфильтровано (8 лист): {name_with_flags}")
            continue

        item = {
            "name": name_with_flags,
            "price": additional_cost(price_val)
        }
        items.append(item)
        print(f"✅ Добавлено: {name_with_flags} → {price_val}")

    print(f"📦 Возвращено позиций (8 лист): {len(items)}")
    return items

# === Публичные функции ===
def fetch_and_process_first_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    ws = client.open_by_key(spreadsheet_id).sheet1
    # Передаём объединённую базу ID в процессор первого листа
    all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}
    return process_first_sheet(ws, all_product_data)

def fetch_and_process_third_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 3:
        raise ValueError(f"Ожидается минимум 3 листа, найдено {len(worksheets)}")
    ws = worksheets[2]  # третий лист — индекс 2
    return process_third_sheet(ws)

def fetch_and_process_fourth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    if len(sh.worksheets()) < 4:
        raise ValueError("Ожидается минимум 4 листа")
    return process_fourth_sheet(sh.worksheets()[3])

def fetch_and_process_fifth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает и обрабатывает 5-й лист с привязкой к product_id.
    """
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 5:
        raise ValueError(f"Ожидается минимум 5 листов, найдено {len(worksheets)}")

    ws = worksheets[4]  # пятый лист

    # Объединённые данные из JSON
    all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}
    print(f"📊 Всего ID в базе: {len(all_product_data)}")

    return process_fifth_sheet(ws, all_product_data)

def fetch_and_process_sixth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 6:
        raise ValueError(f"Ожидается минимум 6 листов, найдено {len(worksheets)}")
    return process_sixth_sheet(worksheets[5])  # шестой лист — индекс 5

def fetch_and_process_eighth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает и обрабатывает 8-й лист Google Таблицы.
    Использует:
      - C: Модификация → как название
      - F: Цена за штуку → как цена
    """
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 8:
        raise ValueError(f"Ожидается минимум 8 листов, найдено {len(worksheets)}")
    
    ws = worksheets[7]  # восьмой лист — индекс 7
    return process_eighth_sheet(ws)

def _extract_name_and_price_ninth_sheet(text: str) -> Optional[Dict[str, Any]]:
    """
    Парсит строки с 9-го листа формата:
        🎧Air Pods 4 - 9200
        Apple Pencil ✏️ pro -9000
        Блок 🔌 20W -1100
        16e 128GB White 🇮🇳 46700   <- без дефиса, но последнее число — цена

    Поддерживает:
      - Эмодзи в начале/середине
      - Пробелы вокруг `-`
      - Отсутствие пробела перед ценой
      - Цена в конце (может быть с ₽)
      - Флаги (остаются в названии)
    """
    if not text or len(text.strip()) < 3:
        return None

    text = text.strip()

    # Удаляем возможные префиксы вроде "[01.04.2026 11:13] Infinity mobile:"
    text = re.sub(r'^\[.*?\]\s*[^:]+:\s*', '', text)

    # Чистим от лишних пробелов
    text = re.sub(r'\s+', ' ', text).strip()

    # Пропускаем заголовки и мусор
    skip_keywords = ["infinity", "mobile", "в наличии", "акция", "скидка"]
    if any(kw in text.lower() for kw in skip_keywords):
        return None

    # 🔍 Попробуем найти шаблон: ... - {цена}
    match_with_dash = re.search(
        r'^(?P<name>.+?)\s*-\s*(?P<price>\d{3,6})\s*[₽рRUB]?$',
        text,
        re.IGNORECASE
    )

    if match_with_dash:
        name_part = match_with_dash.group("name").strip()
        raw_price = match_with_dash.group("price")
    else:
        # Если нет дефиса — попробуем взять последнее число как цену
        price_match = re.search(r'(\d{3,6})\s*[₽рRUB]?$', text)
        if not price_match:
            print(f"❌ Не найдена цена: {text}")
            return None

        raw_price = price_match.group(1)
        name_part = text[:price_match.start()].strip()

    try:
        price_val = int(raw_price)
    except ValueError:
        print(f"❌ Не число: {raw_price}")
        return None

    # Очищаем название
    name = re.sub(r'^[^\w\d]', '', name_part)  # убираем начальные символы
    name = re.sub(r'\s+', ' ', name).strip()

    if not name or len(name) < 3:
        print(f"❌ Слишком короткое имя: '{name}'")
        return None

    return {
        "name": name,
        "price": additional_cost(price_val)
    }
    
def _extract_name_and_price_tenth_sheet(text: str) -> Optional[Dict[str, Any]]:
    """
    Парсит строки с 10-го листа формата:
        Redmi 15C 4/128 Blue🇷🇺 - 7.800
        Note 14 6/128 Green🇪🇺 - 11.500

    Поддерживает:
      - Флаги в названии
      - Десятичные точки как разделитель тысяч
      - Разделение по `-`
    """
    if not text or len(text.strip()) < 5:
        return None

    text = text.strip()

    # Удаляем возможные префиксы вроде "[01.04.2026 12:40] Радиорынок А18:"
    text = re.sub(r'^\[.*?\]\s*[^:]+:\s*', '', text)

    # Чистим лишние пробелы
    text = re.sub(r'\s+', ' ', text).strip()

    # Пропускаем заголовки и мусор
    skip_keywords = ["прайс", "наличие", "🧧", "🔥", "bogatyr", "радиорынок"]
    if any(kw in text.lower() for kw in skip_keywords):
        return None

    # Пропускаем короткие или пустые
    if len(text) < 5:
        return None

    # Ищем шаблон: ... - X.XXX
    match = re.search(
        r'^(?P<name>.+?)\s*-\s*(?P<price>[\d\.]+)\s*[₽рRUB]?$', 
        text, 
        re.IGNORECASE
    )
    if not match:
        print(f"❌ Не найдено название и цена: {text}")
        return None

    name_part = match.group("name").strip()
    raw_price = match.group("price")

    # Убираем точки из цены (7.800 → 7800)
    cleaned_price = raw_price.replace('.', '').replace(',', '')
    if not cleaned_price.isdigit():
        print(f"❌ Цена не число: {raw_price}")
        return None

    try:
        price_val = int(cleaned_price)
    except ValueError:
        print(f"❌ Ошибка парсинга цены: {cleaned_price}")
        return None

    # Чистим название от начальных символов
    name = re.sub(r'^[^\w\d]', '', name_part)
    name = re.sub(r'\s+', ' ', name).strip()

    if not name or len(name) < 3:
        print(f"❌ Слишком короткое имя: '{name}'")
        return None

    return {
        "name": name,
        "price": additional_cost(price_val)
    }

def process_second_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()

    print(f"📊 Всего строк на втором листе: {len(all_values)}")

    for idx, row in enumerate(all_values):
        if not row or not row[0].strip():
            continue

        text = row[0].strip()
        print(f"🔍 Строка {idx}: {text}")  # ← видим, что пришло

        extracted = _extract_name_and_price_dyson(text)
        if extracted:
            items.append({
                "name": extracted["name"],
                "price": extracted["price"]
            })
            print(f"✅ Добавлено: {extracted['name']} → {extracted['price']}")
        else:
            print(f"❌ Пропущено: {text}")

    print(f"📦 Возвращено позиций (2 лист): {len(items)}")
    return items

def process_seventh_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()
    lines = [row[0].strip() for row in all_values if row and row[0].strip()]

    print(f"📊 Обработка седьмого листа: {len(lines)} строк")

    i = 0
    while i < len(lines):
        line = lines[i]

        # Пропускаем чисто графические строки
        if re.match(r'^[-—=]{10,}$', line):
            i += 1
            continue

        extracted = _extract_name_and_price_seventh_sheet(lines, i)

        if extracted:
            items.append(extracted)
            print(f"✅ Добавлено: {extracted['name']} → {extracted['price']}")
            # Если использовали следующую строку как артикул — пропускаем её
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            pn_match = re.search(r'\b\d{3}-\d{5}-\d{2}', next_line) or 'артикул' in next_line.lower()
            if pn_match:
                i += 1
        else:
            print(f"❌ Пропущено: {line}")

        i += 1

    print(f"📦 Возвращено позиций (7 лист): {len(items)}")
    return items

def process_ninth_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()

    print(f"📊 Обработка девятого листа: {len(all_values)} строк")

    all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}
    seen_normalized_names = set()

    for idx, row in enumerate(all_values):
        if not row or not row[0].strip():
            continue

        text = row[0].strip()
        print(f"🔍 [9 лист] Строка {idx}: {text}")

        extracted = _extract_name_and_price_ninth_sheet(text)
        if not extracted:
            print(f"❌ Пропущено: {text}")
            continue

        original_name = extracted["name"]
        normalized_name_for_dup = default_fix_name(original_name)

        # Убираем дубли по нормализованному имени
        if normalized_name_for_dup in seen_normalized_names:
            print(f"🔁 Пропущено (дубль): {original_name}")
            continue
        seen_normalized_names.add(normalized_name_for_dup)

        # Поиск product_id
        to_default_name = default_fix_name(original_name)
        product_id = match_product(to_default_name, all_product_data)

        if not product_id:
            print(f"❌ Нет ID: {to_default_name}")
            continue

        item = {
            "name": original_name,
            "price": extracted["price"],
            "product_id": product_id
        }
        items.append(item)
        print(f"✅ ID {product_id}: {original_name} → {extracted['price']}")

    print(f"📦 Возвращено позиций (9 лист): {len(items)}")
    return items

def process_tenth_sheet(ws) -> List[Dict[str, Any]]:
    items = []
    all_values = ws.get_all_values()

    print(f"📊 Обработка десятого листа: {len(all_values)} строк")

    all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}
    seen_normalized_names = set()

    for idx, row in enumerate(all_values):
        if not row or not row[0].strip():
            continue

        text = row[0].strip()
        print(f"🔍 [10 лист] Строка {idx}: {text}")

        extracted = _extract_name_and_price_tenth_sheet(text)
        if not extracted:
            print(f"❌ Пропущено: {text}")
            continue

        original_name = extracted["name"]
        normalized_name_for_dup = default_fix_name(original_name)

        # Убираем дубли по нормализованному имени
        if normalized_name_for_dup in seen_normalized_names:
            print(f"🔁 Пропущено (дубль): {original_name}")
            continue
        seen_normalized_names.add(normalized_name_for_dup)

        # Поиск product_id
        to_default_name = default_fix_name(original_name)
        product_id = match_product(to_default_name, all_product_data)

        if not product_id:
            print(f"❌ Нет ID: {to_default_name}")
            continue

        item = {
            "name": original_name,
            "price": extracted["price"],
            "product_id": product_id
        }
        items.append(item)
        print(f"✅ ID {product_id}: {original_name} → {extracted['price']}")

    print(f"📦 Возвращено позиций (10 лист): {len(items)}")
    return items

def fetch_and_process_second_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 2:
        raise ValueError(f"Ожидается минимум 2 листа, найдено {len(worksheets)}")
    ws = worksheets[1]  # второй лист
    return process_second_sheet(ws)

def fetch_and_process_seventh_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает и обрабатывает 7-й лист Google Таблицы.
    Использует артикул из следующей строки и добавляет в название.
    """
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 7:
        raise ValueError(f"Ожидается минимум 7 листов, найдено {len(worksheets)}")
    return process_seventh_sheet(worksheets[6])  # индекс 6 — седьмой лист

def fetch_and_process_ninth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает и обрабатывает 9-й лист Google Таблицы.
    Используется для чат-формата типа:
        AirPods 4 - 9200
    """
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 9:
        raise ValueError(f"Ожидается минимум 9 листов, найдено {len(worksheets)}")
    
    ws = worksheets[8]  # девятый лист — индекс 8
    return process_ninth_sheet(ws)

def fetch_and_process_tenth_sheet(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает и обрабатывает 10-й лист Google Таблицы.
    Формат: название - цена (с точкой как разделитель)
    """
    client = gspread.service_account(filename=service_account_file) if service_account_file else gspread.service_account()
    sh = client.open_by_key(spreadsheet_id)
    worksheets = sh.worksheets()
    if len(worksheets) < 10:
        raise ValueError(f"Ожидается минимум 10 листов, найдено {len(worksheets)}")
    
    ws = worksheets[9]  # индекс 9 — десятый лист
    return process_tenth_sheet(ws)

def fetch_and_merge_primary_sheets(spreadsheet_id: str, service_account_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает и объединяет данные с 1, 3, 4 и 5 листов.
    Ищет product_id для всех позиций.
    Оставляет одну позицию на product_id — с минимальной ценой.
    Сохраняет price_min, если есть (для 3-го листа).
    
    Возвращает:
        result: список привязанных товаров
        unlinked_items: список НЕпривязанных товаров (для отладки)
    """
    # Загружаем данные с листов
    sheet1_items = fetch_and_process_first_sheet(spreadsheet_id, service_account_file)
    sheet3_items = fetch_and_process_third_sheet(spreadsheet_id, service_account_file)
    sheet4_items = fetch_and_process_fourth_sheet(spreadsheet_id, service_account_file)
    sheet5_items = fetch_and_process_fifth_sheet(spreadsheet_id, service_account_file)
    eighth_items = fetch_and_process_eighth_sheet(SHEETS_ID_FOR_ORDER, CREDENTIALS_FILE)

    all_items = sheet1_items + sheet3_items + sheet4_items + sheet5_items + eighth_items

    filtered_items = []
    for item in all_items:
        name = item.get("name", "")
        if is_item_allowed(name):
            filtered_items.append(item)
        else:
            print(f"❌ Отфильтровано до привязки: {name}")

    # Загружаем базу ID
    all_product_data = {k: v for d in loaded_data.values() for k, v in d.items()}
    print(f"📊 Всего ID в базе: {len(all_product_data)}")

    merged = {}
    unlinked_items = []  # ← собираем непривязанные

    for item in filtered_items:
        name = item["name"]
        to_default_name = default_fix_name(name)
        product_id = match_product(to_default_name, all_product_data)

        if not product_id:
            # Добавляем в непривязанные
            unlinked_items.append({
                "name": name,
                "price": item["price"],
                "source_price": item.get("price", ""),
                "reason": "No matching product_id"
            })
            continue

        current_price = item["price"]
        new_item = {
            "name": name,
            "price": current_price,
            "product_id": product_id
        }
        if "price_min" in item:
            new_item["price_min"] = item["price_min"]

        if product_id not in merged or current_price < merged[product_id]["price"]:
            merged[product_id] = new_item
        elif current_price == merged[product_id]["price"]:
            if "price_min" in item and ("price_min" not in merged[product_id] or 
                (item["price_min"] < merged[product_id].get("price_min", float('inf')))):
                merged[product_id]["price_min"] = item["price_min"]

    result = list(merged.values())
    result.sort(key=lambda x: _natural_key(x["name"]))

    print(f"📦 Объединено: {len(all_items)} позиций → {len(result)} после привязки к ID")
    print(f"🟡 Не привязано: {len(unlinked_items)} позиций")
    return result, unlinked_items  