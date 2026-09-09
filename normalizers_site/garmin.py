import re
from typing import Any


ARTICLE_PATTERN = re.compile(r"010-\d{5,6}-\d{2}", re.IGNORECASE)


def extract_garmin_article(value: Any) -> str:
    match = ARTICLE_PATTERN.search(str(value or ""))
    return match.group(0).upper() if match else ""


def is_article_row(value: Any) -> bool:
    text = str(value or "").strip()
    article = extract_garmin_article(text)

    if not article:
        return False

    # В строке не должно быть ничего, кроме подписи и артикула
    rest = ARTICLE_PATTERN.sub("", text, count=1)
    rest = re.sub(r"Артикул\s*:?", "", rest, flags=re.IGNORECASE)
    rest = re.sub(r"[_\-\s]", "", rest)

    return not rest


def fix_name_garmin(name: Any) -> str:
    value = str(name or "")

    for symbol in ("💓", "💡", "🚲", "🧭", "⌚️"):
        value = value.replace(symbol, "")

    value = re.sub(r"mm", "", value, flags=re.IGNORECASE)
    value = value.replace("Gen 2 Standart", "Gen 2")

    # Удаляем артикул из исходного текста,
    # потому что он будет добавлен отдельно
    value = re.sub(
        r"\s*Артикул\s*:?\s*010-\d{5,6}-\d{2}[_\s]*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    return re.sub(r"\s+", " ", value).strip()


def return_fix_name_product_garmin(
    name: Any,
    article: Any = "",
) -> str:
    clean_name = fix_name_garmin(name)

    article_value = (
        extract_garmin_article(article)
        or extract_garmin_article(name)
    )

    if article_value and article_value not in clean_name:
        clean_name = f"{clean_name} {article_value}"

    return clean_name.strip()


def return_stock_price_garmin(name: Any) -> str:
    match = re.search(r"-\s*(\d{2,}\s*\d{0,3})$", str(name or ""))

    if not match:
        return ""

    return match.group(1).replace(" ", "")


def is_valid_garmin_price(value: Any) -> bool:
    digits = re.sub(r"\D", "", str(value or ""))
    return len(digits) >= 5


def normalize_garmin_row(
    row: list[Any],
    article: Any = "",
) -> list[Any]:
    if not row:
        return []

    raw_name = str(row[0] or "").strip()

    if not raw_name or is_article_row(raw_name):
        return []

    name = return_fix_name_product_garmin(raw_name, article)

    price = (
        row[1]
        if len(row) > 1 and row[1] not in ("", None)
        else return_stock_price_garmin(raw_name)
    )

    # Артикулы и прочие значения вроде 1, 3013 не являются ценой
    if not is_valid_garmin_price(price):
        return []

    return [name, price]


def normalize_garmin_rows(rows: list[list[Any]]) -> list[list[Any]]:
    result: list[list[Any]] = []
    index = 0

    while index < len(rows):
        row = rows[index]

        if not row or not row[0]:
            index += 1
            continue

        raw_name = str(row[0]).strip()

        # Самостоятельные строки артикулов не являются товарами
        if is_article_row(raw_name):
            index += 1
            continue

        article = ""

        # Артикул обычно находится в следующей строке
        if index + 1 < len(rows):
            next_row = rows[index + 1]

            if next_row and next_row[0] and is_article_row(next_row[0]):
                article = extract_garmin_article(next_row[0])
                index += 1  # пропускаем строку артикула

        normalized = normalize_garmin_row(row, article)

        if normalized:
            result.append(normalized)

        index += 1

    return result