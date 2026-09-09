from typing import Optional, Dict, Any


def _create_filter(
    include: Optional[str] = None,
    exclude: Optional[list] = None,
    name_suffix: Optional[str] = None,
    required_flag: Optional[str] = None,  # может быть строкой или списком
) -> callable:
    """
    Создаёт фильтр:
    :param include: строка или список — что ДОЛЖНО быть в названии (хотя бы одно)
    :param exclude: список — чего НЕ должно быть
    :param name_suffix: имя функции
    :param required_flag: обязательная подстрока или список подстрок (например, ["🇺🇸", "🇨🇳"]) —
                          если указано — проверяется, что **хотя бы один** из них есть в названии
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

    # 🔼 Обработка required_flag как str или list/tuple
    def normalize_flags(flag):
        if flag is None:
            return None
        if isinstance(flag, str):
            return [flag.lower()]
        if isinstance(flag, (list, tuple)):
            return [f.lower() for f in flag]
        return None

    required_flags = normalize_flags(required_flag)

    def filter_func(extracted: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not extracted or not isinstance(extracted, dict):
            return None
        name = extracted.get("name", "").lower()

        # 🔼 Проверка обязательных флагов
        if required_flags and not any(f in name for f in required_flags):
            return None

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
is_airpods = _create_filter(
    include="AirPods",
    exclude=["Max"],
    name_suffix="airpods"
    )
is_airpods_max_2026 = _create_filter(
    include=["AirPods MAX 2", "AirPods MAX 2 (2026)"],
    exclude=["usb-c", "2024"],
    name_suffix="airpods_max"
    )
is_airpods_max_2 = _create_filter(
    include=["AirPods MAX 2024", "AirPods MAX USB-C", "AirPods MAX (USB-C)"],
    exclude=["2026"],
    name_suffix="airpods_max_2"
    )
is_pencil = _create_filter(
    include="Pencil",
    exclude=[],
    name_suffix="pencil"
    )
is_magic = _create_filter(
    include=["Magic Keyboard", "Magic Mouse"],
    exclude=[],
    name_suffix="magic"
    )
is_apple_tv = _create_filter(
    include=["Apple TV"],
    exclude=[],
    name_suffix="apple_tv"
    )

is_aw_se_2 = _create_filter(
    include=["SE (2023) Gen", "SE (2022) Gen", "SE 2", "SE2 4"],
    exclude=["SE (2022) 64", "SE (2022) 128", "SE (2022) 256", "OnePlus", "Mouse", "Sense"],
    name_suffix="aw_se_2"
    )
is_aw_se_3 = _create_filter(
    include=["SE 3", "SE3 4", "SE 2", "SE2 4"],
    exclude=["SE3 128", "SE3 256", "OnePlus", "Mouse", "Sense"],
    name_suffix="aw_se_3"
    )
is_aw_s9 = _create_filter(
    include=["Watch S9", "AW Series 9", "AW 9", "S9 4", "AW  9"],
    exclude=[],
    name_suffix="aw_s9"
    )
is_aw_s10 = _create_filter(
    include=["Watch S10", "AW Series 10", "AW 10", "S10 4", "AW  10"],
    exclude=[],
    name_suffix="aw_s10"
    )
is_aw_s11 = _create_filter(
    include=["Watch S11", "AW Series 11", "AW 11", "S11 4", "AW  11"],
    exclude=[],
    name_suffix="aw_s11"
    )
is_aw_ul_2 = _create_filter(
    include="UL 2",
    exclude=[],
    name_suffix="aw_ul_2"
    )
is_aw_ul_3 = _create_filter(
    include=["UL 3", "Ultra 3"],
    exclude=[],
    name_suffix="aw_ul_3"
    )

is_ipad_9 = _create_filter(
    include="iPad 9",
    exclude=[],
    name_suffix="ipad_9"
    )
is_ipad_10 = _create_filter(
    include="iPad 10",
    exclude=[],
    name_suffix="ipad_10"
    )
is_ipad_11 = _create_filter(
    include="iPad 11",
    exclude=[],
    name_suffix="ipad_11"
    )
is_ipad_mini = _create_filter(
    include={"Mini 6", "Mini 7"},
    exclude=["Mini 64"],
    name_suffix="ipad_mini"
    )
is_ipad_air_5 = _create_filter(
    include="Air 5",
    exclude=["Air 512"],
    name_suffix="ipad_air_5"
    )
is_ipad_air_11 = _create_filter(
    include=["Air 11 M2 ", "Air 11 M3 ", "Air 11 M4 ", "Air 11 M5 "],
    exclude=[
        "neo 13", "air 13 (", "air 15 (", "pro 13 (", "pro 14 (", "pro 16 (", "mly03",
        "mlxx3","mly43","mly23","mly33","mlxw3","mlxy3","mly13","mneh3","mnep3","mnej3","mneq3",
        "mwuv3","mwux3","mwv03","mwv33","mwv53","mwv73","mwv93","mwuu3","mwuw3","mwuy3","mwv13", "mqkp3",
        "mwv43","mwv63","mwv83","muw63","muw73","mrw13","mrw33","mrw43","mrw63","mrw73","mrxv3","mrxw3",
        "mxcv3","mxcu3","mrxt3","mrxu3","mx2g3","mx2k3","mx2v3","mx303","mx2w3","mx313","mx2e3","mx2h3","mx2f3",
        "mx2j3","mx2t3","mx2x3","mx2u3","mx2y3","mde14","mgdr4","mgdu4","mged4","mgea4","mhff4","mdhe4","mdvh4",
        "mhfe4","mhfc4","mhfa4","mhfh4","mhfj4","mhfg4","mhfd4","mde34","mde64","mde54","mgec4","mge64","mge44",
        "mge74","mgee4","mdha4","mdh74","mdhh4","mdhk4","mdhg4","mdhd4","mdh94","mdvk4","mdvn4","mdvf4","mdve4",
        "mdvd4","mdv94","mdva4","mdvc4","mdvu4","mdvt4","mdvq4","mde04","mde44","mdhf4","mdhc4","mdh84","mdhj4",
        "mgdp4","mgdt4","mge94", "mn6y3", "mc6c4", "mc6a4", "mc654", "mc7x4", "mw0y3", "mc6t4", "mc6v4"
        ],
    name_suffix="ipad_air_11"
    )
is_ipad_air_13 = _create_filter(
    include=["Air 13 M2 ", "Air 13 M3 ", "Air 13 M4 ", "Air 13 M5 "],
    exclude=[
        "neo 13", "air 13 (", "air 15 (", "pro 13 (", "pro 14 (", "pro 16 (", "mly03",
        "mlxx3","mly43","mly23","mly33","mlxw3","mlxy3","mly13","mneh3","mnep3","mnej3","mneq3",
        "mwuv3","mwux3","mwv03","mwv33","mwv53","mwv73","mwv93","mwuu3","mwuw3","mwuy3","mwv13", "mqkp3",
        "mwv43","mwv63","mwv83","muw63","muw73","mrw13","mrw33","mrw43","mrw63","mrw73","mrxv3","mrxw3",
        "mxcv3","mxcu3","mrxt3","mrxu3","mx2g3","mx2k3","mx2v3","mx303","mx2w3","mx313","mx2e3","mx2h3","mx2f3",
        "mx2j3","mx2t3","mx2x3","mx2u3","mx2y3","mde14","mgdr4","mgdu4","mged4","mgea4","mhff4","mdhe4","mdvh4",
        "mhfe4","mhfc4","mhfa4","mhfh4","mhfj4","mhfg4","mhfd4","mde34","mde64","mde54","mgec4","mge64","mge44",
        "mge74","mgee4","mdha4","mdh74","mdhh4","mdhk4","mdhg4","mdhd4","mdh94","mdvk4","mdvn4","mdvf4","mdve4",
        "mdvd4","mdv94","mdva4","mdvc4","mdvu4","mdvt4","mdvq4","mde04","mde44","mdhf4","mdhc4","mdh84","mdhj4",
        "mgdp4","mgdt4","mge94", "mn6y3", "mc6c4", "mc6a4", "mc654", "mc7x4", "mw0y3", "mc6t4", "mc6v4"
        ],
    name_suffix="ipad_air_13"
    )
is_ipad_pro_11 = _create_filter(
    include=["Pro 11 M2 ", "Pro 11 M3 ", "Pro 11 M4 ", "Pro 11 M5 "],
    exclude=[],
    name_suffix="ipad_pro_11"
    )
is_ipad_pro_13 = _create_filter(
    include=["Pro 13 M2 ", "Pro 13 M3 ", "Pro 13 M4 ", "Pro 13 M5 "],
    exclude=[
        "neo 13", "air 13 (", "air 15 (", "pro 13 (", "pro 14 (", "pro 16 (", "mly03",
        "mlxx3","mly43","mly23","mly33","mlxw3","mlxy3","mly13","mneh3","mnep3","mnej3","mneq3",
        "mwuv3","mwux3","mwv03","mwv33","mwv53","mwv73","mwv93","mwuu3","mwuw3","mwuy3","mwv13", "mqkp3",
        "mwv43","mwv63","mwv83","muw63","muw73","mrw13","mrw33","mrw43","mrw63","mrw73","mrxv3","mrxw3",
        "mxcv3","mxcu3","mrxt3","mrxu3","mx2g3","mx2k3","mx2v3","mx303","mx2w3","mx313","mx2e3","mx2h3","mx2f3",
        "mx2j3","mx2t3","mx2x3","mx2u3","mx2y3","mde14","mgdr4","mgdu4","mged4","mgea4","mhff4","mdhe4","mdvh4",
        "mhfe4","mhfc4","mhfa4","mhfh4","mhfj4","mhfg4","mhfd4","mde34","mde64","mde54","mgec4","mge64","mge44",
        "mge74","mgee4","mdha4","mdh74","mdhh4","mdhk4","mdhg4","mdhd4","mdh94","mdvk4","mdvn4","mdvf4","mdve4",
        "mdvd4","mdv94","mdva4","mdvc4","mdvu4","mdvt4","mdvq4","mde04","mde44","mdhf4","mdhc4","mdh84","mdhj4",
        "mgdp4","mgdt4","mge94", "mn6y3", "mc6c4", "mc6a4", "mc654", "mc7x4", "mw0y3", "mc6t4", "mc6v4"
        ],
    name_suffix="ipad_pro_13"
    )

is_imac = _create_filter(
    include=[
        "mqh73", "mcr24", "md2q4", "md2t4", "md2p4", "md2w4", "md2u4", "md2v4", "mwuv3", "mwux3", "mwv03", 
        "mwv33", "mwv53", "mwv73", "mwv93", "mwuu3", "mwuw3", "mwuy3", "mwv13", "mwv43", "mwv63", "mwv83", 
        "mwuc3", "mwud3", "mwue3", "mwuf3", "mwug3", "mruh3", "mwuj3", "mqra3", "mqr93", "mqrc3", "mqud3", 
        "mqrt3", "mqrj3", "mqrn3", "mqrq3", "mqup3", "mqrr3", "mquu3", "mqrk3", "mu963"
    ],
    exclude=[],
    name_suffix="imac"
)

is_mac_mini = _create_filter(
    include=["Mac Mini"],
    exclude=[],
    name_suffix="mac_mini"
)

is_macbook = _create_filter(
    include=[
        "neo 13", "air 13 (", "air 15 (", "pro 13 (", "pro 14 (", "pro 16 (", "mly03",
        "mlxx3","mly43","mly23","mly33","mlxw3","mlxy3","mly13","mneh3","mnep3","mnej3","mneq3",
        "mwuv3","mwux3","mwv03","mwv33","mwv53","mwv73","mwv93","mwuu3","mwuw3","mwuy3","mwv13", "mqkp3",
        "mwv43","mwv63","mwv83","muw63","muw73","mrw13","mrw33","mrw43","mrw63","mrw73","mrxv3","mrxw3",
        "mxcv3","mxcu3","mrxt3","mrxu3","mx2g3","mx2k3","mx2v3","mx303","mx2w3","mx313","mx2e3","mx2h3","mx2f3",
        "mx2j3","mx2t3","mx2x3","mx2u3","mx2y3","mde14","mgdr4","mgdu4","mged4","mgea4","mhff4","mdhe4","mdvh4",
        "mhfe4","mhfc4","mhfa4","mhfh4","mhfj4","mhfg4","mhfd4","mde34","mde64","mde54","mgec4","mge64","mge44",
        "mge74","mgee4","mdha4","mdh74","mdhh4","mdhk4","mdhg4","mdhd4","mdh94","mdvk4","mdvn4","mdvf4","mdve4",
        "mdvd4","mdv94","mdva4","mdvc4","mdvu4","mdvt4","mdvq4","mde04","mde44","mdhf4","mdhc4","mdh84","mdhj4",
        "mgdp4","mgdt4","mge94", "mn6y3", "mc6c4", "mc6a4", "mc654", "mc7x4", "mw0y3", "mc6t4", "mc6v4", "mw123",
        "mw0w3"
    ],
    exclude=[],
    name_suffix="macbook"
)

is_iphone_11 = _create_filter(
    include=["11 64", "11 128"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_11"
    )
is_iphone_12 = _create_filter(
    include=["12 64", "12 128", "12 256"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_12"
    )
is_iphone_13 = _create_filter(
    include=["13 128", "13 256", "13 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_13"
    )
is_iphone_14 = _create_filter(
    include=["14 128", "14 256", "14 512", "14 Plus"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_14"
    )
is_iphone_14 = _create_filter(
    include=["14 128", "14 256", "14 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_14"
    )
is_iphone_14_plus = _create_filter(
    include=["14 Plus 128", "14 Plus 256", "14 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_14_plus"
    )
is_iphone_15_eSim = _create_filter(
    include=["15 128", "15 256", "15 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_15",
    required_flag="🇺🇸"
    )
is_iphone_15_1Sim = _create_filter(
    include=["15 128", "15 256", "15 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_15"
    )
is_iphone_15_Dual = _create_filter(
    include=["15 128", "15 256", "15 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_15",
    required_flag=["🇭🇰", "🇨🇳"]
    )
is_iphone_15_plus_eSim = _create_filter(
    include=["15 Plus 128", "15 Plus 256", "15 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_15_plus",
    required_flag="🇺🇸"
    )
is_iphone_15_plus_1Sim = _create_filter(
    include=["15 Plus 128", "15 Plus 256", "15 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_15_plus"
    )
is_iphone_15_plus_Dual = _create_filter(
    include=["15 Plus 128", "15 Plus 256", "15 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_15_plus",
    required_flag=["🇭🇰", "🇨🇳"]
    )
is_iphone_15_pro_eSim = _create_filter(
    include=["15 Pro 128", "15 Pro 256", "15 Pro 512", "15 Pro 1Tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_15_pro",
    required_flag="🇺🇸"
    )
is_iphone_15_pro_1Sim = _create_filter(
    include=["15 Pro 128", "15 Pro 256", "15 Pro 512", "15 Pro 1Tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_15_pro"
    )
is_iphone_15_pro_Dual = _create_filter(
    include=["15 Pro 128", "15 Pro 256", "15 Pro 512", "15 Pro 1Tb"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_15_pro",
    required_flag=["🇭🇰", "🇨🇳"]
    )
is_iphone_15_pro_max_eSim = _create_filter(
    include=["15 Pro Max 256", "15 Pro Max 512", "15 Pro Max 1Tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_15_pro_max",
    required_flag="🇺🇸"
    )
is_iphone_15_pro_max_1Sim = _create_filter(
    include=["15 Pro Max 256", "15 Pro Max 512", "15 Pro Max 1Tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_15_pro_max"
    )
is_iphone_15_pro_max_Dual = _create_filter(
    include=["15 Pro Max 256", "15 Pro Max 512", "15 Pro Max 1Tb"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_15_pro_max",
    required_flag=["🇭🇰", "🇨🇳"]
    )

is_iphone_16e_eSim = _create_filter(
    include=["16Е 128", "16Е 256", "16Е 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_16e",
    required_flag="🇺🇸"
    )
is_iphone_16e_1Sim = _create_filter(
    include=["16Е 128", "16Е 256", "16Е 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_16e"
    )
is_iphone_16e_Dual = _create_filter(
    include=["16Е 128", "16Е 256", "16Е 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_16e",
    required_flag=["🇭🇰", "🇨🇳",]
    )
is_iphone_16_eSim = _create_filter(
    include=["16 128", "16 256", "16 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_16",
    required_flag="🇺🇸"
    )
is_iphone_16_1Sim = _create_filter(
    include=["16 128", "16 256", "16 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_16"
    )
is_iphone_16_Dual = _create_filter(
    include=["16 128", "16 256", "16 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_16",
    required_flag=["🇭🇰", "🇨🇳",]
    )
is_iphone_16_plus_eSim = _create_filter(
    include=["16 Plus 128", "16 Plus 256", "16 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_16_plus",
    required_flag="🇺🇸"
    )
is_iphone_16_plus_1Sim = _create_filter(
    include=["16 Plus 128", "16 Plus 256", "16 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_16_plus"
    )
is_iphone_16_plus_Dual = _create_filter(
    include=["16 Plus 128", "16 Plus 256", "16 Plus 512"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_16_plus",
    required_flag=["🇭🇰", "🇨🇳",]
    )
is_iphone_16_pro_eSim = _create_filter(
    include=["16 Pro 128", "16 Pro 256", "16 Pro 512", "16 Pro 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_16_pro",
    required_flag="🇺🇸"
    )
is_iphone_16_pro_1Sim = _create_filter(
    include=["16 Pro 128", "16 Pro 256", "16 Pro 512", "16 Pro 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_16_pro"
    )
is_iphone_16_pro_Dual = _create_filter(
    include=["16 Pro 128", "16 Pro 256", "16 Pro 512", "16 Pro 1tb"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_16_pro",
    required_flag=["🇭🇰", "🇨🇳",]
    )
is_iphone_16_pro_max_eSim = _create_filter(
    include=["16 Pro Max 256", "16 Pro Max 512", "16 Pro Max 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳"],
    name_suffix="iphone_16_pro_max",
    required_flag="🇺🇸"
    )
is_iphone_16_pro_max_1Sim = _create_filter(
    include=["16 Pro Max 256", "16 Pro Max 512", "16 Pro Max 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "🇭🇰", "🇨🇳", "🇺🇸"],
    name_suffix="iphone_16_pro_max"
    )
is_iphone_16_pro_max_Dual = _create_filter(
    include=["16 Pro Max 256", "16 Pro Max 512", "16 Pro Max 1tb"],
    exclude=["Air", "iPad", "asis", "CPO"],
    name_suffix="iphone_16_pro_max",
    required_flag=["🇭🇰", "🇨🇳",]
    )
is_iphone_17_e_1Sim = _create_filter(
    include=["17e 256", "17e 512", "17e 1tb"],
    exclude=["iPad", "asis", "CPO", "(eSim)", "Dual"],
    name_suffix="iphone_17_e_1Sim"
    )
is_iphone_17_e_eSim = _create_filter(
    include=["17e 256", "17e 512", "17e 1tb"],
    exclude=["iPad", "asis", "CPO", "1Sim", "Dual"],
    name_suffix="iphone_17_e_eSim"
    )
is_iphone_17_e_Dual = _create_filter(
    include=["17e 256", "17e 512", "17e 1tb"],
    exclude=["iPad", "asis", "CPO", "1Sim", "eSim"],
    name_suffix="iphone_17_e_eSim"
    )
is_iphone_17_air = _create_filter(
    include=["17 air 256", "17 air 512", "17 air 1tb"],
    exclude=["iPad", "asis", "CPO"],
    name_suffix="iphone_17_air"
    )
is_iphone_17_1Sim = _create_filter(
    include=["17 256", "17 512"],
    exclude=["Air", "iPad", "asis", "CPO", "(eSim)", "Dual"],
    name_suffix="iphone_17"
    )
is_iphone_17_eSim = _create_filter(
    include=["17 256", "17 512"],
    exclude=["Air", "iPad", "asis", "CPO", "1Sim", "Dual"],
    name_suffix="iphone_17"
    )
is_iphone_17_Dual = _create_filter(
    include=["17 256", "17 512"],
    exclude=["Air", "iPad", "asis", "CPO", "1Sim", "eSim"],
    name_suffix="iphone_17"
    )
is_iphone_17_pro_eSim = _create_filter(
    include=["17 Pro 256", "17 Pro 512", "17 Pro 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "1Sim", "Dual"],
    name_suffix="iphone_17_pro"
    )
is_iphone_17_pro_1Sim = _create_filter(
    include=["17 Pro 256", "17 Pro 512", "17 Pro 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "(eSim)", "Dual"],
    name_suffix="iphone_17_pro"
    )
is_iphone_17_pro_Dual = _create_filter(
    include=["17 Pro 256", "17 Pro 512", "17 Pro 1tb"],
    exclude=["Air", "iPad", "asis", "CPO", "1Sim", "eSim"],
    name_suffix="iphone_17_pro"
    )
is_iphone_17_pro_max_eSim = _create_filter(
    include=["17 Pro Max 256", "17 Pro Max 512", "17 Pro Max 1tb", "17 Pro Max 2tb"],
    exclude=["Air", "iPad", "asis", "CPO", "1Sim", "Dual"],
    name_suffix="iphone_17_pro_max"
    )
is_iphone_17_pro_max_1Sim = _create_filter(
    include=["17 Pro Max 256", "17 Pro Max 512", "17 Pro Max 1tb", "17 Pro Max 2tb"],
    exclude=["Air", "iPad", "asis", "CPO", "(eSim)", "Dual"],
    name_suffix="iphone_17_pro_max"
    )
is_iphone_17_pro_max_Dual = _create_filter(
    include=["17 Pro Max 256", "17 Pro Max 512", "17 Pro Max 1tb", "17 Pro Max 2tb", "1Sim", "eSim"],
    exclude=["Air", "iPad", "asis", "CPO", "1Sim", "eSim"],
    name_suffix="iphone_17_pro_max"
    )