import re

def clean_sunrise_text(text: str) -> str:
    """
    Извлекает строки с товарами из текста Sunrise.
    Фильтрует заголовки, ссылки и служебные сообщения.
    
    Ожидается, что товарные строки имеют формат:
    `🇪🇺 Название - Цена`
    или
    `🇪🇺 Название - Цена [ссылка]`
    
    Возвращает только чистые строки товара.
    """
    if not text:
        return ""

    lines = text.split('\n')
    product_lines = []
    
    # Паттерн для поиска строки товара:
    # 1. Может начинаться с любых символов (ссылки, эмодзи и т.д.)
    # 2. Важная часть: ищем область, заключенную в обратные кавычки `...`
    # 3. Внутри кавычек должно быть: (Название) - (Цифры)
    
    # Альтернативный подход: 
    # Ищем строки, которые содержат обратные кавычки.
    # Затем внутри них ищем паттерн "текст - цена".
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        
        # 1. Быстрая фильтрация по наличию обратных кавычек.
        # Если кавычек нет, скорее всего, это служебная строка (типа "Актуально..." или ссылки на фото)
        if '`' not in clean_line:
            continue

        # 2. Извлекаем содержимое между первыми найденными обратными кавычками.
        # Регулярка ищет содержимое между ` и `.
        match = re.search(r'`([^`]+)`', clean_line)
        
        if not match:
            continue
            
        content_in_ticks = match.group(1).strip()
        
        # 3. Проверяем, что извлеченный контент похож на товар (содержит цену в конце после тире)
        # Паттерн: Нечто ... - Цифры
        # Тире может быть обычным '-' или длинным '–'.
        price_pattern = re.compile(r'.*[-–—]\s*\d+$')
        
        if price_pattern.search(content_in_ticks):
            product_lines.append(content_in_ticks)

    return '\n'.join(product_lines)

def clean_sunrise_text_to_rows(text: str) -> list:
    """
    Вспомогательная функция, которая сразу возвращает список строк для вставки в Google Sheets.
    """
    cleaned_text = clean_sunrise_text(text)
    rows = []
    
    if not cleaned_text:
        return rows
        
    for line in cleaned_text.split('\n'):
        line = line.strip()
        if line:
            # Берем весь текст в ячейку A, ячейку B оставляем пустой
            rows.append([line, ""])
            
    return rows