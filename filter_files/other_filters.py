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
is_dgi = _create_filter(
    include="DJI",
    exclude=[],
    name_suffix="dgi"
    )
is_gopro = _create_filter(
    include="GoPro",
    exclude=[],
    name_suffix="gopro"
    )
is_jbl = _create_filter(
    include="JBL",
    exclude=[],
    name_suffix="jbl"
    )
is_marshall = _create_filter(
    include="Marshall",
    exclude=[],
    name_suffix="marshall"
    )
is_beats = _create_filter(
    include="Beats",
    exclude=[],
    name_suffix="beats"
    )
is_plaud = _create_filter(
    include="Plaud",
    exclude=[],
    name_suffix="plaud"
    )

is_huawei = _create_filter(
    include="Huawei",
    exclude=[],
    name_suffix="huawei"
    )
is_tecno = _create_filter(
    include="Tecno",
    exclude=[],
    name_suffix="tecno"
    )
is_yandex = _create_filter(
    include="Яндекс",
    exclude=[],
    name_suffix="yandex"
)
is_realme = _create_filter(
    include="Realme",
    exclude=[],
    name_suffix="realme"
)

is_pixel_buds = _create_filter(
    include="Pixel Buds",
    exclude=[],
    name_suffix="pixel_buds"
    )
is_pixel_watch = _create_filter(
    include="Pixel Watch",
    exclude=[],
    name_suffix="pixel_watch"
    )
is_pixel_phone = _create_filter(
    include="Pixel",
    exclude=["Buds", "Watch", "Tab"],
    name_suffix="pixel_phone"
)
is_pixel_tab = _create_filter(
    include="Pixel Tab",
    exclude=[],
    name_suffix="pixel_tab"
    )
is_sony_phone = _create_filter(
    include="Sony",
    exclude=["Play", "Sense"],
    name_suffix="sony_phone"
)
is_asus = _create_filter(
    include="Asus",
    exclude=[],
    name_suffix="asus"
    )

is_oneplus_buds = _create_filter(
    include="OnePlus Buds",
    exclude=[],
    name_suffix="oneplus_buds"
    )
is_oneplus_watch = _create_filter(
    include="OnePlus Watch",
    exclude=[],
    name_suffix="oneplus_watch"
    )
is_oneplus_phone = _create_filter(
    include="OnePlus",
    exclude=["Buds", "Watch", "Tab"],
    name_suffix="oneplus_phone"
)
is_oneplus_tab = _create_filter(
    include="OnePlus Tab",
    exclude=[],
    name_suffix="oneplus_tab"
    )
is_zte = _create_filter(
    include="ZTE",
    exclude=[],
    name_suffix="zte"
    )
is_nothing_phone = _create_filter(
    include="Nothing Phone",
    exclude=[],
    name_suffix="nothing_phone"
    )
is_nothing_ear = _create_filter(
    include="Nothing Ear",
    exclude=[],
    name_suffix="nothing_ear"
    )
is_honor = _create_filter(
    include="Honor",
    exclude=[],
    name_suffix="honor"
    )

is_nintendo = _create_filter(
    include="Nintendo",
    exclude=[],
    name_suffix="nintendo"
)
is_oculus = _create_filter(
    include=["Oculus", "Quest", "Meta"],
    exclude=["Ray-Ban"],
    name_suffix="oculus"
    )
is_pico = _create_filter(
    include="Pico",
    exclude=[],
    name_suffix="pico"
    )
is_playstation = _create_filter(
    include="PlayStation",
    exclude=[],
    name_suffix="playstation"
    )
is_dualsense = _create_filter(
    include="sense",
    exclude=[],
    name_suffix="dualsense"
    )
is_xbox = _create_filter(
    include="Xbox",
    exclude=[],
    name_suffix="xbox"
    )
is_steam = _create_filter(
    include="Steam",
    exclude=[],
    name_suffix="steam"
    )
is_rayban = _create_filter(
    include="Ray-Ban",
    exclude=[],
    name_suffix="rayban"
    )

