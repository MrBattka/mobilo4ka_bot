from typing import Optional, Dict, Any

# def _create_filter(keyword: str, name_suffix: str = None) -> callable:
#     """
#     Создаёт фильтр, который ищет `keyword` в названии товара.
#     :param keyword: строка для поиска, например "Galaxy A"
#     :param name_suffix: имя функции (опционально, для читаемости в отладке)
#     """
#     series_name = name_suffix or keyword.replace(" ", "_")

#     def filter_func(extracted: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
#         if not extracted or not isinstance(extracted, dict):
#             return None
#         name = extracted.get("name", "")
#         if keyword in name:
#             return extracted
#         return None

#     filter_func.__name__ = f"is_{series_name}_series"
#     return filter_func

def _create_filter(
    include: Optional[str] = None,
    exclude: Optional[list] = None,
    name_suffix: Optional[str] = None
) -> callable:
    """
    Создаёт фильтр:
    :param include: строка или список — что ДОЛЖНО быть в названии (хотя бы одно)
    :param exclude: список — чего НЕ должно быть
    :param name_suffix: имя функции
    """
    series_name = name_suffix or (isinstance(include, str) and include or "custom").replace(" ", "_")
    exclude = [e.lower() for e in exclude] if exclude else []
    if include is not None:
        if isinstance(include, str):
            include_list = [include.lower()]
        else:
            include_list = [i.lower() for i in include]
    else:
        include_list = []

    def filter_func(extracted: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not extracted or not isinstance(extracted, dict):
            return None
        name = extracted.get("name", "").lower()

        # Проверяем, что ничего из exclude нет
        for ex in exclude:
            if ex in name:
                return None

        # Если include пуст — считаем, что подходит (фильтр-заглушка)
        if not include_list:
            return extracted

        # Проверяем, что хотя бы одно вхождение из include есть
        if any(inc in name for inc in include_list):
            return extracted

        return None

    filter_func.__name__ = f"is_{series_name}_series"
    return filter_func

is_galaxy_a = _create_filter(
    include=["A16 ", "A17 ", "A25 ", "A26 ", "A27 ", "A35 ", "A36 ", "A37 ", "A55 ", "A56 ", "A57 "],
    exclude=["iPad"],
    name_suffix="samsung_a"
    )

is_galaxy_s = _create_filter(
    include=["S23 ", "S24 ", "S25 ", "S26 "],
    exclude=[],
    name_suffix="samsung_s"
    )

is_galaxy_z = _create_filter(
    include=["Z Fold ", "Z Flip"],
    exclude=[],
    name_suffix="samsung_z"
    )

is_galaxy_buds = _create_filter(
    include="Galaxy Buds",
    exclude=[],
    name_suffix="galaxy_buds"
    )

is_galaxy_watch = _create_filter(
    include=["Watch 7", "Watch 8"],
    exclude=[],
    name_suffix="galaxy_watch"
    )

is_galaxy_tab = _create_filter(
    include="Galaxy Tab",
    exclude=[],
    name_suffix="galaxy_tab"
    )

is_apple = _create_filter(
    include="Apple",
    exclude=[],
    name_suffix="apple"
    )