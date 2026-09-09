import os
import re
import math
import time
import random
import json
from gspread.exceptions import APIError
import argparse
from typing import Optional, Tuple, List, Dict, Any
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
def authenticate(credentials_file: str,
                 scopes: List[str] = SCOPES) -> Credentials:
    """
    Авторизация строго через Service Account.
    Ожидает JSON-файл сервисного аккаунта в credentials_file.
    В случае отсутствия/некорректного файла — возбуждает исключение.
    """
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(f"Service account file not found: {credentials_file}")
    try:
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=scopes)
    except Exception as e:
        raise RuntimeError(f"Failed to load service account credentials: {e}") from e
    return creds

def normalize_gopro(name: str) -> str:
    name_clean = re.sub(r'\s+', ' ', name.strip(), flags=re.I)
    match = re.match(r'(?i)(go\s*pro\s+hero)(?:\s+(\d+))?(.*)', name_clean)
    if not match:
        return name_clean

    prefix = "Go Pro HERO"
    suffix = match.group(3).strip()

    # Удаляем лишние слова
    suffix = re.sub(r'\b(Edition|Ed\.?|Pro|Camera|Action Camera|акция|камера)\b', '', suffix, flags=re.I)
    # Убираем лишние пробелы и дефисы
    suffix = re.sub(r'\s+', ' ', suffix).strip(' -')
    
    return f"{prefix} {suffix}".strip() if suffix else prefix

def connect_gspread(creds: Credentials) -> gspread.Client:
    """Авторизовать gspread клиент."""
    return gspread.authorize(creds)


def parse_memory(name: str) -> Tuple[Optional[int], Optional[int], str]:
    """
    Возвращает (ram_gb_or_None, storage_gb_or_None, cleaned_name).
    Правило: если форма A/B и B без единицы:
      - 32, 64, 128, 256, 512 => GB
      - 1, 2 => TB (1024GB, 2048GB)
    Иначе используем указанные единицы.
    """
    s = name or ""
    s_norm = s.replace('\xa0', ' ')
    pattern = re.search(r'(\d+)\s*(GB|G|TB|T)?\s*[\/\-]\s*(\d+)\s*(GB|G|TB|T)?', s_norm, flags=re.IGNORECASE)
    if pattern:
        a, a_unit, b, b_unit = pattern.group(1), pattern.group(2), pattern.group(3), pattern.group(4)
        ram = int(a)
        b_val = int(b)
        
        if b_unit:
            # Если явно указана единица
            bu = b_unit.upper()
            storage = b_val * 1024 if 'T' in bu else b_val
        else:
            # Если единица не указана, определяем по значению
            if b_val in (32, 64, 128, 256, 512):
                storage = b_val  # GB
            elif b_val == 1:
                storage = b_val * 1024  # TB в GB
            elif b_val == 2:
                storage = b_val * 2048  # TB в GB
            else:
                # Для остальных чисел — предполагаем GB
                storage = b_val
        
        cleaned = (s_norm[:pattern.start()] + s_norm[pattern.end():]).strip()
        return ram, storage, cleaned

    pattern2 = re.search(r'(\d+)\s*(GB|G|TB|T)\b', s_norm, flags=re.IGNORECASE)
    if pattern2:
        val, unit = int(pattern2.group(1)), pattern2.group(2).upper()
        storage = val * 1024 if 'T' in unit else val
        cleaned = (s_norm[:pattern2.start()] + s_norm[pattern2.end():]).strip()
        return None, storage, cleaned

    return None, None, s_norm.strip()

def detect_color_from_name(name: str) -> Optional[str]:
    colors = ['black', 'white', 'blue', 'red', 'gold', 'silver', 'green', 'grey', 'gray', 'pink', 'purple', 'yellow']
    for c in colors:
        if re.search(r'\b' + re.escape(c) + r'\b', name, flags=re.IGNORECASE):
            return c.lower()
    return None


def normalize_number(s: str, allow_zero: bool = False) -> Optional[float]:
    if not s:
        return None
    s2 = re.sub(r'[^\d\-,\.]', '', s)
    s2 = s2.replace(' ', '').replace(',', '.')
    if s2 in ('', '.', '-', '-.', None):
        return None
    try:
        v = float(s2)
        if not allow_zero and v == 0:
            return None
        return v
    except:
        return None


def format_price(value: Optional[float]) -> str:
    if value is None:
        return ""
    v = round(float(value), 2)
    if v.is_integer():
        return str(int(v))
    s = ('{:.2f}'.format(v)).rstrip('0').rstrip('.')
    return s


def detect_columns(headers: List[str]) -> Tuple[int, int, int]:
    h_map = {h.strip().lower(): i for i, h in enumerate(headers)}
    def col_index(name_candidates):
        for n in name_candidates:
            if n in h_map:
                return h_map[n]
        return None
    idx_name = col_index(['name', 'название', 'model'])
    idx_price = col_index(['price', 'цена'])
    idx_minus = col_index(['minus', 'вычет', 'delta'])
    return idx_name, idx_price, idx_minus


def build_data_rows(rows: List[List[str]], idx_name: int, idx_price: int, idx_minus: int) -> List[Dict]:
    data_rows = []
    for i, row in enumerate(rows[1:], start=2):
        name = row[idx_name].strip() if idx_name < len(row) else ""
        price_raw = row[idx_price].strip() if (idx_price is not None and idx_price < len(row)) else ""
        minus_raw = row[idx_minus].strip() if (idx_minus is not None and idx_minus < len(row)) else ""
        price = normalize_number(price_raw, allow_zero=False)
        minus = normalize_number(minus_raw, allow_zero=True)
        if minus is None:
            minus = 0.0
        ram, storage, cleaned = parse_memory(name)
        color = detect_color_from_name(name)
        base_candidate = cleaned or name
        
        base_candidate = re.sub(r'\s+', ' ', base_candidate).strip().lower()
        base_candidate = normalize_gopro(base_candidate)
        if color:
            base_candidate = re.sub(r'\b' + re.escape(color) + r'\b', '', base_candidate, flags=re.IGNORECASE).strip()
            base_candidate = re.sub(r'\s+', ' ', base_candidate).strip()
        
        data_rows.append({
            'row': i,
            'orig_name': name,
            'base_name': base_candidate,
            'color': (color or '').lower(),
            'price': price,
            'minus': minus,
            'ram': ram,
            'storage': storage
        })
    return data_rows


def generate_updates(data_rows: List[Dict], price_col_idx_1based: int) -> List[Tuple[int, int, str]]:
    groups = {}
    for r in data_rows:
        key = (r['base_name'], r['color'])
        groups.setdefault(key, []).append(r)
    
    updates: List[Tuple[int, int, str]] = []
    
    for key, items in groups.items():
        base_name, color = key

        # Определяем, является ли группа Go Pro HERO
        is_gopro = re.match(r'(?i)go\s*pro\s+hero', base_name)

        def sort_key(it):
            # Если это Go Pro — сортируем по номеру модели (из orig_name)
            if is_gopro:
                match = re.search(r'hero\s+(\d+)', it['orig_name'], re.I)
                model_num = int(match.group(1)) if match else 0
                return (1, model_num)  # сортировка по model_num, если Go Pro
            else:
                # Иначе — как раньше: по RAM и storage
                ramv = it['ram'] if it['ram'] is not None else -math.inf
                storv = it['storage'] if it['storage'] is not None else -math.inf
                return (0, ramv, storv)

        items_sorted = sorted(items, key=sort_key, reverse=True)
        
        # Отладка
        print(f"\nGroup: {key}")
        for it in items_sorted:
            print(f"  {it['orig_name']}: ram={it['ram']}, storage={it['storage']}, price={it['price']}, minus={it['minus']}")
        
        # Сначала передаём цены между разными конфигурациями памяти
        memory_configs = {}
        for it in items_sorted:
            mem_key_tuple = (it['ram'], it['storage'])
            if mem_key_tuple not in memory_configs:
                memory_configs[mem_key_tuple] = []
            memory_configs[mem_key_tuple].append(it)
        
        # Отладка: покажи порядок конфигураций
        print(f"  Memory configs order:")
        for mem_config in sorted(memory_configs.keys(), reverse=True):
            print(f"    {mem_config}")
        
        # Обновляем цены между конфигурациями (от большей к меньшей)
        current_price = None
        for mem_config in sorted(memory_configs.keys(), reverse=True):
            mem_items = memory_configs[mem_config]
            print(f"  Processing Memory config: ram={mem_config[0]}, storage={mem_config[1]}")
            
            # Ищем цену в текущей конфигурации
            found_price_in_config = False
            temp_price = current_price
            
            for it in mem_items:
                if it['price'] is not None and it['price'] > 0:
                    temp_price = it['price']
                    found_price_in_config = True
                    print(f"    -> Found price: {temp_price}")
                    break
            
            # Если нет цены в текущей конфигурации, применяем цену от более мощной
            if not found_price_in_config and temp_price is not None:
                print(f"    -> Using price from higher config: {temp_price}")
                for it in mem_items:
                    new_price = round(temp_price - it.get('minus', 0.0), 2)
                    val_str = format_price(new_price)
                    updates.append((it['row'], price_col_idx_1based, val_str))
                    print(f"    -> Applying: {it['orig_name']}, new_price={new_price}, val_str={val_str}")
                    temp_price = new_price
            else:
                # Применяем цену внутри конфигурации (от одного цвета к другим)
                for it in mem_items:
                    if it['price'] is not None and it['price'] > 0:
                        temp_price = it['price']
                        print(f"    -> Found price: {temp_price}")
                    else:
                        if temp_price is not None:
                            new_price = round(temp_price - it.get('minus', 0.0), 2)
                            val_str = format_price(new_price)
                            updates.append((it['row'], price_col_idx_1based, val_str))
                            print(f"    -> Applying: {it['orig_name']}, new_price={new_price}, val_str={val_str}")
                            temp_price = new_price
            
            # Сохраняем цену для следующей (меньшей) конфигурации
            current_price = temp_price
    
    return updates

def _colnum_to_letter(n: int) -> str:
    s = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        s = chr(65 + rem) + s
    return s


def apply_updates(ws: Any, updates: List[Tuple[int, int, str]]) -> int:
    """
    Отправляет обновления пакетами через values_batch_update.
    Возвращает число успешно применённых записей.
    """
    ss = ws.spreadsheet  # gspread.Spreadsheet
    sheet_name = ws.title
    quoted_sheet = f"'{sheet_name}'" if " " in sheet_name or any(c in sheet_name for c in "!'") else sheet_name

    # подготовить data для batch
    data_entries = []
    for row, col, val in updates:
        col_letter = _colnum_to_letter(col)
        cell_ref = f"{quoted_sheet}!{col_letter}{row}"
        data_entries.append({"range": cell_ref, "values": [[val]]})

    applied = 0
    # отправляем партиями, чтобы не превысить размер запроса и уменьшить число write-запросов
    chunk_size = 100  # можно увеличить/уменьшить в зависимости от лимитов
    max_retries = 5
    for i in range(0, len(data_entries), chunk_size):
        chunk = data_entries[i:i + chunk_size]
        body = {"valueInputOption": "USER_ENTERED", "data": chunk}
        for attempt in range(max_retries):
            try:
                ss.values_batch_update(body)  # единый запрос для всех ячеек в chunk
                applied += len(chunk)
                break
            except APIError as e:
                # при 429 — exponential backoff и повтор
                err_text = str(e)
                if "429" in err_text or "Quota exceeded" in err_text:
                    sleep_time = (2 ** attempt) + random.random()
                    print(f"Quota exceeded, retry in {sleep_time:.1f}s (attempt {attempt+1}/{max_retries})")
                    time.sleep(sleep_time)
                    continue
                # остальные ошибки — пробрасываем
                raise
        else:
            # если не удалось после retry — лог и продолжить дальше
            print(f"Failed to apply chunk starting at index {i}, skipped {len(chunk)} updates.")
    return applied

def process_sheet(sheet_key: str, credentials_file: str,
                  apply: bool = False) -> Tuple[List[Tuple[int, int, str]], int]:
    """Главная функция: возвращает список подготовленных обновлений и количество применённых записей."""
    creds = authenticate(credentials_file)
    gc = connect_gspread(creds)
    sh = gc.open_by_key(sheet_key)
    ws = sh.sheet1
    rows = ws.get_all_values()
    if not rows or len(rows) < 2:
        return [], 0
    headers = rows[0]
    idx_name, idx_price, idx_minus = detect_columns(headers)
    # если не найдены заголовки — назначаем первые 3 столбца
    if idx_name is None or idx_price is None or idx_minus is None:
        max_cols = max(len(r) for r in rows)
        if max_cols < 3:
            raise SystemExit("В таблице меньше 3 колонок — невозможно назначить name/price/minus автоматически")
        idx_name = 0 if idx_name is None else idx_name
        idx_price = 1 if idx_price is None else idx_price
        idx_minus = 2 if idx_minus is None else idx_minus
    data_rows = build_data_rows(rows, idx_name, idx_price, idx_minus)
    price_col_idx_1based = idx_price + 1
    updates = generate_updates(data_rows, price_col_idx_1based)
    applied = 0
    if updates and apply:
        applied = apply_updates(ws, updates)
    return updates, applied


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fill missing prices from highest-memory sibling')
    parser.add_argument('--sheet', required=False, default='1fni43Tj5fuqPWh8Ftd7LQ_L9i7mmIlW9OLhb68FBge8',
                        help='Google Sheet ID (default: встроенный)')
    parser.add_argument('--credentials', required=False, default='price-from-base-f801bdfcf2d1.json', help='service account JSON file')
    parser.add_argument('--apply', action='store_true', help='Применить изменения в таблице (по умолчанию dry-run)')
    args = parser.parse_args()

    updates_list, applied_count = process_sheet(sheet_key=args.sheet,
                                               credentials_file=args.credentials,
                                               apply=args.apply)
    if not updates_list:
        print("Ничего не нужно менять (ни одно правило не сгенерировало обновлений).")
    else:
        print(f"Найдено {len(updates_list)} потенциальных обновлений. Примеры (row, col, value):")
        for row, col, val in updates_list[:50]:
            print(f"  row={row}, col={col}, value={val}")
        if args.apply:
            print(f"Применено {applied_count} обновлений.")