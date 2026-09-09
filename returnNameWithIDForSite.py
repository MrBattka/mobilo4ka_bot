import json
import os
import re
from typing import List, Dict, Any, Optional
from data.articleToIdMap import ARTICLE_TO_ID_MAP
from defaultFixName import default_fix_name


DATA_DIR = os.path.join(os.path.dirname(__file__), "data/site_data")

def load_product_data(filename: str) -> Dict[str, Dict]:
    """Загружает JSON файл с данными товаров"""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return {}

def match_product_for_site(item_name: str, product_data: Dict[str, Dict]) -> Optional[str]:
    if not item_name or not product_data:
        return None
        
    item_lower = item_name.lower()
    
    for product_id, rules in product_data.items():
        include_list = rules.get("include", [])
        exclude_list = rules.get("exclude", [])
        
        # ⚠️ Если include ПУСТ - пропускаем этот ID полностью
        if not include_list:
            continue
        
        # ✅ Все элементы include ДОЛЖНЫ быть в названии товара
        # Используем все() вместо any()
        include_match = all(
            keyword.lower() in item_lower 
            for keyword in include_list
        )
        
        # Если не все элементы совпали - пропускаем этот ID
        if not include_match:
            continue
        
        # Если есть exclude - исключаем товар при совпадении
        if exclude_list:
            exclude_match = any(
                keyword.lower() in item_lower 
                for keyword in exclude_list
            )
            # Если exclude совпал - пропускаем этот ID
            if exclude_match:
                continue
        
        # Если мы здесь - товар полностью совпал со всеми условиями
        return product_id
    
    article_match = re.search(
        r"010-\d{5,6}-\d{2}",
        item_name,
        flags=re.IGNORECASE,
    )
    
    if article_match:
        article = article_match.group(0).upper()
        return ARTICLE_TO_ID_MAP.get(article)

    return None

def filter_items_by_product_ids(
    items: List[Dict[str, Any]], 
    json_files: List[str]
) -> List[Dict[str, Any]]:
    """
    Фильтрует товары по выбранным JSON файлам.
    Возвращает только товары, которые привязались к id
    """
    result = []
    
    # Загружаем все данные
    all_product_data = {}
    for json_file in json_files:
        product_data = load_product_data(json_file)
        all_product_data.update(product_data)
    
    for item in items:
        item_name = item.get("name", "")
        product_id = match_product_for_site(defaultFixName(item_name), all_product_data)
        
        if product_id:
            # Добавляем найденный id в товар
            item_copy = item.copy()
            item_copy["product_id"] = product_id
            result.append(item_copy)
    
    return result

# Пример использования с вашим кодом
if __name__ == "__main__":
    # Загружаем товары из таблицы
    from indexPriceFromOrder import fetch_and_process_first_sheet
    
    sheets_id = '1UwXYXKT6A0AqneKIwvDgYgSqMyy5RWEEBTXHHjyKkFs'
    credentials_file = "price-from-base-39198cff139d.json"
    
    items = fetch_and_process_first_sheet(sheets_id, credentials_file)
    
    # Фильтруем по выбранным JSON файлам
    selected_files = [
        "idProductAppleData.json",
        "idProductXiaomiData.json",
        "idProductSamsungData.json",
        "idProductGarminData.json",
        "idProductOtherBrandData.json",
        "idProductOtherBrandData2.json"
    ]
    
    filtered_items = filter_items_by_product_ids(items, selected_files)
    
    # Выводим результаты
    for item in filtered_items:
        print(f"ID: {item['product_id']}, Название: {item['name']}, Цена: {item['price']}")