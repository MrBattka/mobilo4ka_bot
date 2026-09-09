import gspread
import asyncio
import re
from typing import Dict, Optional
from utils.helpers import checkUsed
from indexPriceFromOrder import fetch_and_process_ninth_sheet, fetch_and_process_tenth_sheet, fetch_and_process_eighth_sheet


async def update_column_g_in_sheet_async(credentials_file: str, spreadsheet_url: str) -> str:
    """
    Асинхронное обновление колонки G (Опт) на 5-м листе.
    - Привязка товаров через product_id (по названию)
    - Использует рыночные цены С ТОЛЬКО с 9 и 10 листов
    - Обновляет ЦЕНУ ТОЛЬКО если товар ЕСТЬ на 9 или 10 листе И УЖЕ ЕСТЬ цена в G
    - Не трогает б/у (только по checkUsed)
    - Возвращает подробный отчёт
    """
    try:
        gc = gspread.service_account(filename=credentials_file)
        sh = gc.open_by_url(spreadsheet_url)

        sheet5 = sh.get_worksheet(4)  # 5-й лист
        data5 = sheet5.get_all_values()

        if len(data5) < 2:
            return "❌ Лист 5 пуст или нет данных."

        headers5 = data5[0]

        # === Определяем колонки ===
        idx_cost = find_col(headers5, ['Себестоимость', 'Cost'])
        idx_g = find_col(headers5, ['G', 'Цена', 'Price']) or 6  # G = индекс 6
        idx_name_5 = find_col(headers5, ['Наименование', 'Name']) or 2  # C — Наименование

        if idx_cost is None:
            return "❌ Не найдена колонка 'Себестоимость' на 5 листе."

        # === Загружаем рыночные цены с 9 и 10 листов + привязываем к product_id ===
        eighth_items = fetch_and_process_eighth_sheet(sh.id, credentials_file)
        ninth_items = fetch_and_process_ninth_sheet(sh.id, credentials_file)
        tenth_items = fetch_and_process_tenth_sheet(sh.id, credentials_file)

        # Собираем price_map: product_id → market_price
        price_map: Dict[str, float] = {}
        for item in eighth_items + ninth_items + tenth_items:
            pid = item.get("product_id")
            price = item.get("price")
            if pid and price:
                if pid not in price_map or price > price_map[pid]:
                    price_map[pid] = price

        # Если нет рыночных данных — нечего обновлять
        if not price_map:
            return "🟡 Нет данных с 9 и 10 листов для привязки цен."

        # === Загружаем данные 5-го листа с привязкой к product_id ===
        from returnNameWithID import match_product
        from defaultFixName import default_fix_name as fix_name_for_id
        all_product_data = {k: v for d in [await load_json_data()] for k, v in d.items()}

        # 🔽 ДОБАВЛЕНО: Собираем все товары и группируем по нормализованному имени для выравнивания себестоимости
        items_by_normalized_name = {}

        # Первый проход: собираем все строки и нормализуем имена
        for row_idx, row in enumerate(data5[1:], start=2):
            if len(row) <= max(idx_cost, idx_name_5):
                continue

            cost_str = row[idx_cost].strip()
            raw_name = row[idx_name_5].strip() if len(row) > idx_name_5 else ""

            # Пропускаем Б/У и ненужные категории
            if checkUsed(raw_name) or re.search(r'\b(Left|Right|Case)\b', raw_name, re.IGNORECASE):
                continue

            if not raw_name or not cost_str:
                continue

            norm_name = fix_name_for_id(raw_name)
            try:
                cost_value = float(cost_str.replace(',', '.'))
            except:
                cost_value = 0.0

            # Группируем по нормализованному имени
            if norm_name not in items_by_normalized_name:
                items_by_normalized_name[norm_name] = {
                    "names": [],           # оригинальные названия
                    "costs": [],           # все себестоимости
                    "max_cost": 0.0,       # будет максимальная себестоимость
                    "rows": []             # информация о строках: (row_index, current_g_value, raw_name)
                }
            items_by_normalized_name[norm_name]["names"].append(raw_name)
            items_by_normalized_name[norm_name]["costs"].append(cost_value)
            items_by_normalized_name[norm_name]["rows"].append({
                "row_idx": row_idx,
                "g_col_val": row[idx_g] if len(row) > idx_g else '',
                "raw_name": raw_name
            })

        # Второй проход: определяем максимальную себестоимость для каждой группы
        for key in items_by_normalized_name:
            items_by_normalized_name[key]["max_cost"] = max(items_by_normalized_name[key]["costs"])

        # === Основной цикл обработки строк с обновлённой логикой себестоимости ===
        updates = []
        MARKUP_COEFF = 1.02
        applied_count = 0
        failed_items = []
        skipped_items = []
        no_price_items = [] 
        updated_items = [] 

        for row_idx, row in enumerate(data5[1:], start=2):
            if len(row) <= max(idx_cost, idx_name_5):
                continue
            
            cost_str = row[idx_cost].strip()
            raw_name = row[idx_name_5].strip() if len(row) > idx_name_5 else ""
        
            # 🔴 Пропускаем Б/У
            if checkUsed(raw_name):
                print(f"🔁 Пропущено (б/у): {raw_name}")
                continue
            
            # 🔴 Пропускаем, если в названии есть Left, Right или Case
            if re.search(r'\b(Left|Right|Case)\b', raw_name, re.IGNORECASE):
                print(f"🔁 Пропущено (ключевое слово): {raw_name}")
                continue
            
            if not raw_name or not cost_str:
                continue

            norm_name = fix_name_for_id(raw_name)
            group = items_by_normalized_name.get(norm_name)
            if not group:
                continue  # на всякий случай

            # Используем МАКСИМАЛЬНУЮ себестоимость из группы одинаковых товаров
            try:
                cost_value = group["max_cost"]
            except:
                cost_value = 0.0

            # 🔍 Привязываем к product_id
            product_id = match_product(norm_name, all_product_data)

            if not product_id:
                failed_items.append(raw_name)
                print(f"❌ Нет ID: {raw_name}")
                continue

            # 🔎 Есть ли товар на 9/10 листах?
            market_price = price_map.get(product_id)
            if not market_price:
                skipped_items.append(raw_name)
                print(f"🟡 Нет на рынке: {raw_name} (ID: {product_id})")
                continue

            # 🔎 Проверяем, есть ли уже цена в колонке G
            current_g_value = row[idx_g] if len(row) > idx_g else ''
            if not current_g_value or current_g_value.strip() == '':
                no_price_items.append(raw_name)
                print(f"⚠️ Нет цены в G: {raw_name}")
                continue

            try:
                current_price = float(current_g_value.replace(',', '.'))
            except:
                no_price_items.append(raw_name)
                print(f"⚠️ Некорректная цена в G: {raw_name}")
                continue

            # Только если всё ок — считаем новую цену
            final_price = market_price
            
            if market_price > cost_value:
                final_price = market_price * MARKUP_COEFF
            else:
                final_price = market_price

            # 🔴 КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Цена не может быть ниже себестоимости
            if final_price < cost_value:
                final_price = cost_value  # Поднимаем до уровня себестоимости
                
            final_price = -(-final_price // 100) * 100

            # Фиксируем изменение (только если отличается более чем на 1 рубль)
            if abs(final_price - current_price) > 1:
                updated_items.append({
                    "name": raw_name,
                    "old_price": int(current_price),
                    "new_price": int(final_price)
                }) 

            # Обновляем G
            cell_range = f"G{row_idx}"
            updates.append({
                "range": cell_range,
                "values": [[round(final_price, 2)]]
            })
            applied_count += 1


        # Применяем обновления
        if updates:
            sheet5.batch_update(updates, value_input_option='USER_ENTERED')

        # === Формируем отчёт ===
        result_lines = []

        # ✅ Обновлённые
        if updated_items:
            result_lines.append("🟢 Обновлены цены (на основе рыночных данных):")
            for item in updated_items[:50]:
                result_lines.append(f"• {item['name']} → {item['new_price']} ₽ (было: {item['old_price']})")
            if len(updated_items) > 50:
                result_lines.append(f"… и ещё {len(updated_items) - 50}")

        # ❌ Нет цены в G
        if no_price_items:
            result_lines.append("\n❌ Нет цены в колонке G (пропущены):")
            for name in no_price_items[:20]:
                result_lines.append(f"• {name}")
            if len(no_price_items) > 20:
                result_lines.append(f"… и ещё {len(no_price_items) - 20}")

        # ⚠️ Есть ID, но нет на рынке
        if skipped_items:
            result_lines.append("\n🟡 Найдены в базе, но отсутствуют на рынке (9/10 листы):")
            for name in skipped_items[:20]:
                result_lines.append(f"• {name}")
            if len(skipped_items) > 20:
                result_lines.append(f"… и ещё {len(skipped_items) - 20}")

        # 🔴 Без ID
        if failed_items:
            result_lines.append("\n🔴 Не удалось привязать (нет ID):")
            for name in failed_items[:20]:
                result_lines.append(f"• {name}")
            if len(failed_items) > 20:
                result_lines.append(f"… и ещё {len(failed_items) - 20}")

        # 📊 Итог
        total_processed = len(data5) - 1
        summary = f"\n📊 <b>Итого:</b> Обработано {total_processed}, обновлено {applied_count}."
        if not updated_items and not no_price_items and not skipped_items and not failed_items:
            summary += " Нет изменений."
        result_lines.append(summary)

        return "\n".join(result_lines)

    except Exception as e:
        return f"❌ Ошибка: {type(e).__name__}: {e}"


# === Вспомогательные функции ===

def find_col(headers: list, candidates: list) -> Optional[int]:
    """Находит индекс колонки по списку возможных названий."""
    for c in candidates:
        if c in headers:
            return headers.index(c)
        if c.lower() in [h.lower() for h in headers]:
            return [h.lower() for h in headers].index(c.lower())
    return None


async def load_json_data():
    """Загружает объединённые данные из JSON файлов"""
    import json
    from config.settings import DATA_DIR, SELECTED_FILES
    all_data = {}
    for filename in SELECTED_FILES:
        file_path = DATA_DIR / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                all_data.update(json.load(f))
    return all_data