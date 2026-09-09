from typing import Optional, Dict, Any


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

# === Определяем фильтры ===
is_mi_phone = _create_filter(
    include="MI ",
    exclude=["Mi Watch", "Mi Pad", "Mi Port", "HDMI", "Redmi", "Note"],
    name_suffix="mi_phone"
    )
is_mi_pad = _create_filter(
    include="Mi Pad",
    exclude=["Redmi", "Huawei"],
    name_suffix="mi_pad"
    )
is_redmi_buds = _create_filter(
    include="Redmi Buds",
    exclude=[],
    name_suffix="redmi_buds"
    )
is_redmi_watch = _create_filter(
    include="Redmi Watch",
    exclude=[],
    name_suffix="redmi_watch"
    )
is_redmi_phone = _create_filter(
    include=["Note", "Redmi", "Redmi Note"],
    exclude=["Buds", "Huawei", "Pad", "Watch", "Plaud"],
    name_suffix="redmi_phone"
    )
is_redmi_pad = _create_filter(
    include="Redmi Pad",
    exclude=["Huawei"],
    name_suffix="redmi_pad"
    )

is_poco_phone = _create_filter(
    include="Poco",
    exclude=["Pad"],
    name_suffix="poco_phone"
    )
is_poco_pad = _create_filter(
    include="Poco Pad",
    exclude=[],
    name_suffix="poco_pad"
    )