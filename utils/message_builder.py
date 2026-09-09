from datetime import date
from indexPriceFromOrder import format_section


def build_header():
    d = date.today()
    return (f"{d.day:02d}.{d.month:02d}.{d.year}"
            '\n🧑‍💻Работаем с 9:00 до 20:00'
            '\n🚀Доставка'
            '\n❗️В наличии в Севастополе'
            '\n💸Оплата наличными при получении'
            '\n'
            '\n💬*ДЛЯ ЗАКАЗА*💬'
            '\n𓂃✍︎ ⌯⌲ * https://t.me/m0bilo4ka *')

def build_header_for_order():
    d = date.today()
    return (f"{d.day:02d}.{d.month:02d}.{d.year}"
            '\n'
            '\n🧑‍💻 Работаем: 11:00 - 20:00'
            '\n❗Сб-Вс - Выходные❗'
            '\n\n📍Москва, Багратионовский проезд 7к20В, БЦ '
            '\n«Конвент-Плюс»'
            '\n'
            '\n💬ДЛЯ ЗАКАЗА💬'
            '\n🚀Telegram: @onlinemyprice')
    
def build_info_price_order():
    return ('🧑‍💻 Работаем: 11:00 - 20:00'
            '\n❗Сб-Вс - Выходные❗'
            '\n\n📍Москва, Багратионовский проезд 7к20В, БЦ «Конвент-Плюс»'
            '\n'
            '\n✈️ Отправка в регионы в день заказа'
            '\n'
            '\n🛃 Виды расчета:'
            '\n • Наличными'
            '\n • Снятием с вашей карты'
            '\n • USDT'
            '\n • QR на снятие'
            '\n'
            '\n····●·○·●·○·●·○·●·○·●····'
            '\n💬 ДЛЯ ЗАКАЗА 💬'
            '\n🚀 Telegram: @onlinemyprice'
            '\n'
            '\n✈️ <b>Наши отправки</b>'
            '\n🚀 Telegram: t.me/mobilochka_delivery')
    
def build_header_message_17_iphone():
    return ('<b>Поддержка сим-карт на iPhone 17 / Pro / Pro Max</b>'
            '\n<i>Только eSim</i> - 🇧🇭🇨🇦🇬🇺🇯🇵🇰🇼🇲🇽🇴🇲🇶🇦🇸🇦🇦🇪🇺🇸🇻🇮'
            '\n<i>Nano-Sim + eSim</i> - 🇪🇺🇮🇳🇻🇳🇦🇺🇳🇿🇰🇷🇸🇬🇭🇰'
            '\n<i>Dual Nano-Sim</i> - 🇨🇳'
            '\n<b>17 Air</b> - <i>только eSim</i>'
            '\n'
            '\n'
            '\n')
    
def build_header_message_14_iphone():
    return ('<i>🇨🇳🇭🇰🇸🇬 ( 2 sim ) 🇸🇬 бывает sim + e sim</i>'
            '\n<i>🇺🇸 от 14 Модели - e sim ( нет лотка sim )</i>'
            '\n<i>Остальные страны sim + e sim</i>'
            '\n'
            '\n'
            '\n')
    
def build_footer_message_for_order():
    return ('\n····●·○·●·○·●·○·●·○·●····'
            '\n💬<b>ДЛЯ ЗАКАЗА</b>💬'
            '\n🚀Telegram: @onlinemyprice'
            '\n'
            '\n✈️ <b>Наши отправки</b>'
            '\n🚀Telegram: t.me/mobilochka_delivery')
    
def build_info_dyson():
    return ('\n\n🇪🇺🇰🇷 - <i>Наша вилка</i>'
            '\n🇨🇳🇬🇧🇲🇾🇦🇺🇭🇰🇸🇬🇦🇪🇸🇦 - <i>Не наша вилка</i>')
    
def build_info_about_price():
    d = date.today()
    return ('<b>Добрый день</b>\n\n'
           f'<i>{d.day:02d}.{d.month:02d}.{d.year}</i>'
            '\n\n<b>✔️Прайс обновлен✔️</b>')

def create_order_keyboard(**ids):
    base = "https://t.me/c/2384328012/"
    buttons = [
        [{"text": "📢 Инфо", "url": base + str(ids.get("header"))}],
        [{"text": "📱 iPhone", "url": base + str(ids.get("iphone"))}],
        [{"text": "📱 Samsung", "url": base + str(ids.get("samsung"))}],
        [{"text": "✍️ Заказать", "url": "https://t.me/onlinemyprice"}],
    ]
    return {"inline_keyboard": buttons}

def build_garmin(is_dji, garmin_items, is_gopro,
                 is_jbl, is_marshall, is_beats, is_plaud):
    return (
        format_section('⌚️', '<b>DJI</b>', is_dji) +
        format_section('⌚️', '<b>Garmin</b>', garmin_items) +
        format_section('📸', '<b>GoPro</b>', is_gopro) +
        format_section('🔊', '<b>JBL</b>', is_jbl) +
        format_section('🎧', '<b>Marshall</b>', is_marshall) +
        format_section('🎧', '<b>Beats</b>', is_beats) +
        format_section('🎙️', '<b>Plaud</b>', is_plaud) +
        build_footer_message_for_order()
    )

def build_huawei(is_huawei, is_tecno, is_yandex, is_realme):
    return (
        format_section('📱', '<b>Huawei</b>', is_huawei) +
        format_section('📱', '<b>Tecno</b>', is_tecno) +
        format_section('🔊', '<b>Яндекс</b>', is_yandex) +
        format_section('📱', '<b>Realme</b>', is_realme) +
        build_footer_message_for_order()
    )
    
def build_google(is_pixel_buds, is_pixel_watch, is_pixel_phone,
                 is_pixel_tab, is_sony_phone, is_asus):
    return (
        format_section('🎧', '<b>Pixel Buds</b>', is_pixel_buds) +
        format_section('⌚', '<b>Pixel Watch</b>', is_pixel_watch) +
        format_section('📱', '<b>Pixel Phone</b>', is_pixel_phone) +
        format_section('📟', '<b>Pixel Tablet</b>', is_pixel_tab) +
        format_section('📱', '<b>Sony</b>', is_sony_phone) +
        format_section('📱', '<b>Asus</b>', is_asus) +
        build_footer_message_for_order()
    )
        
def build_nothing(is_oneplus_buds, is_oneplus_watch, is_oneplus_phone,
                 is_oneplus_tab, is_zte, is_nothing_phone, is_nothing_ear, is_honor):
    return (
        format_section('🎧', '<b>OnePlus Buds</b>', is_oneplus_buds) +
        format_section('⌚', '<b>OnePlus Watch</b>', is_oneplus_watch) +
        format_section('📱', '<b>OnePlus Phone</b>', is_oneplus_phone) +
        format_section('📟', '<b>OnePlus Tablet</b>', is_oneplus_tab) +
        format_section('📱', '<b>ZTE</b>', is_zte) +
        format_section('📱', '<b>Nothing Phone</b>', is_nothing_phone) +
        format_section('🎧', '<b>Nothing Ear</b>', is_nothing_ear) +
        format_section('📱', '<b>Honor</b>', is_honor) +
        build_footer_message_for_order()
    )
    
def build_game(is_nintendo, is_oculus, is_pico, is_playstation,
               is_dualsense, is_xbox, is_steam, is_rayban):
    return (
        format_section('🕹️', '<b>Nintendo</b>', is_nintendo) +
        format_section('🥽', '<b>Oculus</b>', is_oculus) +
        format_section('🥽', '<b>Pico</b>', is_pico) +
        format_section('🥽', '<b>Ray-Ban</b>', is_rayban) +
        format_section('🎮', '<b>Playstation</b>', is_playstation) +
        format_section('🎮', '<b>DualSense</b>', is_dualsense) +
        format_section('📱', '<b>Xbox</b>', is_xbox) +
        format_section('📱', '<b>Steam</b>', is_steam) +
        build_footer_message_for_order()
    )
    
def build_xiaomi(is_mi_phone, is_redmi_buds, is_redmi_watch,
               is_redmi_phone):
    return (
        format_section('📱', '<b>Mi Phone</b>', is_mi_phone) +
        format_section('🎧', '<b>Redmi Buds</b>', is_redmi_buds) +
        format_section('⌚', '<b>Redmi Watch</b>', is_redmi_watch) +
        format_section('📱', '<b>Redmi Phone</b>', is_redmi_phone) +
        build_footer_message_for_order()
    )
    
def build_poco(is_poco_phone, is_poco_pad, is_redmi_pad, is_mi_pad):
    return (
        format_section('📱', '<b>Poco Phone</b>', is_poco_phone) +
        format_section('📟', '<b>Poco Pad</b>', is_poco_pad) +
        format_section('📟', '<b>Mi Pad</b>', is_mi_pad) +
        format_section('📟', '<b>Redmi Pad</b>', is_redmi_pad) +
        build_footer_message_for_order()
    )  
    
def build_airpods(is_airpods, is_airpods_max_2, is_airpods_max_2026,
                  is_pencil, is_magic, is_apple_tv):
    return (
        format_section('🎧', '<b>AirPods</b>', is_airpods) +
        format_section('🎧', '<b>AirPods Max 2024</b>', is_airpods_max_2) +
        format_section('🎧', '<b>AirPods Max 2026</b>', is_airpods_max_2026) +
        format_section('✏️', '<b>Pencil</b>', is_pencil) +
        format_section('🖱️⌨️', '<b>Magic</b>', is_magic) +
        format_section('📺', '<b>Apple TV</b>', is_apple_tv) +
        build_footer_message_for_order()
    )
    
def build_aw(is_aw_se_2, is_aw_se_3, is_aw_s9,
                  is_aw_s10, is_aw_s11, is_aw_ul_2,
                  is_aw_ul_3):
    return (
        format_section('⌚', '<b>AW SE 2</b>', is_aw_se_2) +
        format_section('⌚', '<b>AW SE 3</b>', is_aw_se_3) +
        format_section('⌚', '<b>AW S9</b>', is_aw_s9) +
        format_section('⌚', '<b>AW S10</b>', is_aw_s10) +
        format_section('⌚', '<b>AW S11</b>', is_aw_s11) +
        format_section('⌚', '<b>AW Ultra 2</b>', is_aw_ul_2) +
        format_section('⌚', '<b>AW Ultra 3</b>', is_aw_ul_3) +
        build_footer_message_for_order()
    )
    
def build_ipad(is_ipad_9, is_ipad_10, is_ipad_11,
                  is_ipad_mini, is_ipad_air_5, is_ipad_air_11,
                  is_ipad_air_13, is_ipad_pro_11, is_ipad_pro_13):
    return (
        format_section('📟', '<b>iPad 9</b>', is_ipad_9) +
        format_section('📟', '<b>iPad 10</b>', is_ipad_10) +
        format_section('📟', '<b>iPad 11</b>', is_ipad_11) +
        format_section('📟', '<b>iPad Mini</b>', is_ipad_mini) +
        format_section('📟', '<b>iPad Air 5</b>', is_ipad_air_5) +
        format_section('📟', '<b>iPad Air 11</b>', is_ipad_air_11) +
        format_section('📟', '<b>iPad Air 13</b>', is_ipad_air_13) +
        format_section('📟', '<b>iPad Pro 11</b>', is_ipad_pro_11) +
        format_section('📟', '<b>iPad Pro 13</b>', is_ipad_pro_13) +
        build_footer_message_for_order()
    )
    
def build_macbook(is_mac_mini, is_imac, is_macbook):
    return (
        format_section('🖥️', '<b>Mac Mini</b>', is_mac_mini) +
        format_section('🖥️', '<b>iMac</b>', is_imac) +
        format_section('💻', '<b>MacBook</b>', is_macbook) +
        build_footer_message_for_order()
    )
    
def build_iphone_11_15(filtered_iphone_11, filtered_iphone_12, filtered_iphone_13,
                      filtered_iphone_14, filtered_iphone_14_plus,
                      filtered_iphone_15_eSim, filtered_iphone_15_1Sim, filtered_iphone_15_Dual,
                      filtered_iphone_15_plus_eSim, filtered_iphone_15_plus_1Sim, filtered_iphone_15_plus_Dual,
                      filtered_iphone_15_pro_eSim, filtered_iphone_15_pro_1Sim, filtered_iphone_15_pro_Dual,
                      filtered_iphone_15_pro_max_eSim, filtered_iphone_15_pro_max_1Sim, filtered_iphone_15_pro_max_Dual):
    
    parts = [build_header_message_14_iphone()] 
    
    has_15 = filtered_iphone_15_eSim or filtered_iphone_15_1Sim or filtered_iphone_15_Dual
    has_15_plus = filtered_iphone_15_plus_eSim or filtered_iphone_15_plus_1Sim or filtered_iphone_15_plus_Dual
    has_15_pro = filtered_iphone_15_pro_eSim or filtered_iphone_15_pro_1Sim or filtered_iphone_15_pro_Dual
    has_15_pro_max = filtered_iphone_15_pro_max_eSim or filtered_iphone_15_pro_max_1Sim or filtered_iphone_15_pro_max_Dual
    
    if filtered_iphone_11:
        parts.append(format_section('📱', '<b>iPhone 11</b>', filtered_iphone_11))
    if filtered_iphone_12:
        parts.append(format_section('📱', '<b>iPhone 12</b>', filtered_iphone_12))
    if filtered_iphone_13:
        parts.append(format_section('📱', '<b>iPhone 13</b>', filtered_iphone_13))
    if filtered_iphone_14:
        parts.append(format_section('📱', '<b>iPhone 14</b>', filtered_iphone_14))
    if filtered_iphone_14_plus:
        parts.append(format_section('📱', '<b>iPhone 14 Plus</b>', filtered_iphone_14_plus))
    if has_15:
        parts.append('<b>📱 iPhone 15</b>\n')
        if filtered_iphone_15_eSim:
            parts.append(format_section('', '', filtered_iphone_15_eSim))
        if filtered_iphone_15_1Sim:
            parts.append(format_section('', '', filtered_iphone_15_1Sim))
        if filtered_iphone_15_Dual:
            parts.append(format_section('', '', filtered_iphone_15_Dual))
    if has_15_plus:
        parts.append('<b>📱 iPhone 15 Plus</b>\n')
        if filtered_iphone_15_plus_eSim:
            parts.append(format_section('', '', filtered_iphone_15_plus_eSim))
        if filtered_iphone_15_plus_1Sim:
            parts.append(format_section('', '', filtered_iphone_15_plus_1Sim))
        if filtered_iphone_15_plus_Dual:
            parts.append(format_section('', '', filtered_iphone_15_plus_Dual))
    if has_15_pro:
        parts.append('<b>📱 iPhone 15 Pro</b>\n')
        if filtered_iphone_15_pro_eSim:
            parts.append(format_section('', '', filtered_iphone_15_pro_eSim))
        if filtered_iphone_15_pro_1Sim:
            parts.append(format_section('', '', filtered_iphone_15_pro_1Sim))
        if filtered_iphone_15_pro_Dual:
            parts.append(format_section('', '', filtered_iphone_15_pro_Dual))
    if has_15_pro_max:
        parts.append('<b>📱 iPhone 15 Pro Max</b>\n')
        if filtered_iphone_15_pro_max_eSim:
            parts.append(format_section('', '', filtered_iphone_15_pro_max_eSim))
        if filtered_iphone_15_pro_max_1Sim:
            parts.append(format_section('', '', filtered_iphone_15_pro_max_1Sim))
        if filtered_iphone_15_pro_max_Dual:
            parts.append(format_section('', '', filtered_iphone_15_pro_max_Dual))
    
    parts.append(build_footer_message_for_order())
    return "".join(parts)
    
    
def build_iphone_16(filtered_16e_eSim, filtered_16e_1Sim, filtered_16e_Dual,
                    filtered_16_eSim, filtered_16_1Sim, filtered_16_Dual,
                    filtered_16_plus_eSim, filtered_16_plus_1Sim, filtered_16_plus_Dual,
                    filtered_16_pro_eSim, filtered_16_pro_1Sim, filtered_16_pro_Dual,
                    filtered_16_pro_max_eSim, filtered_16_pro_max_1Sim, filtered_16_pro_max_Dual):
    
    has_16e = filtered_16e_eSim or filtered_16e_1Sim or filtered_16e_Dual
    has_16 = filtered_16_eSim or filtered_16_1Sim or filtered_16_Dual
    has_16_plus = filtered_16_plus_eSim or filtered_16_plus_1Sim or filtered_16_plus_Dual
    has_16_pro = filtered_16_pro_eSim or filtered_16_pro_1Sim or filtered_16_pro_Dual
    has_16_pro_max = filtered_16_pro_max_eSim or filtered_16_pro_max_1Sim or filtered_16_pro_max_Dual
    
    parts = []
    
    if has_16e:
        parts.append('<b>📱 iPhone 16e</b>\n')
        if filtered_16e_eSim:
            parts.append(format_section('', '', filtered_16e_eSim))
        if filtered_16e_1Sim:
            parts.append(format_section('', '', filtered_16e_1Sim))
        if filtered_16e_Dual:
            parts.append(format_section('', '', filtered_16e_Dual))
    
    if has_16:
        parts.append('<b>📱 iPhone 16</b>\n')
        if filtered_16_eSim:
            parts.append(format_section('', '', filtered_16_eSim))
        if filtered_16_1Sim:
            parts.append(format_section('', '', filtered_16_1Sim))
        if filtered_16_Dual:
            parts.append(format_section('', '', filtered_16_Dual))
    
    if has_16_plus:
        parts.append('<b>📱 iPhone 16 Plus</b>\n')
        if filtered_16_plus_eSim:
            parts.append(format_section('', '', filtered_16_plus_eSim))
        if filtered_16_plus_1Sim:
            parts.append(format_section('', '', filtered_16_plus_1Sim))
        if filtered_16_plus_Dual:
            parts.append(format_section('', '', filtered_16_plus_Dual))
            
    if has_16_pro:
        parts.append('<b>📱 iPhone 16 Pro</b>\n')
        if filtered_16_pro_eSim:
            parts.append(format_section('', '', filtered_16_pro_eSim))
        if filtered_16_pro_1Sim:
            parts.append(format_section('', '', filtered_16_pro_1Sim))
        if filtered_16_pro_Dual:
            parts.append(format_section('', '', filtered_16_pro_Dual))
            
    if has_16_pro_max:
        parts.append('<b>📱 iPhone 16 Pro Max</b>\n')
        if filtered_16_pro_max_eSim:
            parts.append(format_section('', '', filtered_16_pro_max_eSim))
        if filtered_16_pro_max_1Sim:
            parts.append(format_section('', '', filtered_16_pro_max_1Sim))
        if filtered_16_pro_max_Dual:
            parts.append(format_section('', '', filtered_16_pro_max_Dual))
    
    parts.append(build_footer_message_for_order())
    return "".join(parts)
    
    
def build_iphone_17(filtered_17_e_1Sim, filtered_17_e_eSim, filtered_17_e_Dual,
                    filtered_17_air, filtered_17_eSim, filtered_17_1Sim, filtered_17_Dual,
                    filtered_17_Pro_eSim, filtered_17_Pro_1Sim, filtered_17_Pro_Dual,
                    filtered_17_Pro_Max_eSim, filtered_17_Pro_Max_1Sim, filtered_17_Pro_Max_Dual):
    parts = [build_header_message_17_iphone()]

    has_17e = filtered_17_e_eSim or filtered_17_e_1Sim or filtered_17_e_Dual
    has_17 = filtered_17_eSim or filtered_17_1Sim or filtered_17_Dual
    has_17_Pro = filtered_17_Pro_eSim or filtered_17_Pro_1Sim or filtered_17_Pro_Dual
    has_17_Pro_Max = filtered_17_Pro_Max_eSim or filtered_17_Pro_Max_1Sim or filtered_17_Pro_Max_Dual
    
    if has_17e:
        parts.append('<b>📱 iPhone 17e</b>\n')
        if filtered_17_e_eSim:
            parts.append(format_section('', '', filtered_17_e_eSim))
        if filtered_17_e_1Sim:
            parts.append(format_section('', '', filtered_17_e_1Sim))
        if filtered_17_e_Dual:
            parts.append(format_section('', '', filtered_17_e_Dual))

    if filtered_17_air:
        parts.append(format_section('📱', '<b>iPhone 17 Air</b>', filtered_17_air))
    if has_17:
        parts.append('<b>📱 iPhone 17</b>\n')
        if filtered_17_eSim:
            parts.append(format_section('', '', filtered_17_eSim))
        if filtered_17_1Sim:
            parts.append(format_section('', '', filtered_17_1Sim))
        if filtered_17_Dual:
            parts.append(format_section('', '', filtered_17_Dual))
    if has_17_Pro:
        parts.append('<b>📱 iPhone 17 Pro</b>\n')
        if filtered_17_Pro_eSim:
            parts.append(format_section('', '', filtered_17_Pro_eSim))
        if filtered_17_Pro_1Sim:
            parts.append(format_section('', '', filtered_17_Pro_1Sim))
        if filtered_17_Pro_Dual:
            parts.append(format_section('', '', filtered_17_Pro_Dual))
    if has_17_Pro_Max:
        parts.append('<b>📱 iPhone 17 Pro Max</b>\n')
        if filtered_17_Pro_Max_eSim:
            parts.append(format_section('', '', filtered_17_Pro_Max_eSim))
        if filtered_17_Pro_Max_1Sim:
            parts.append(format_section('', '', filtered_17_Pro_Max_1Sim))
        if filtered_17_Pro_Max_Dual:
            parts.append(format_section('', '', filtered_17_Pro_Max_Dual))

    parts.append(build_footer_message_for_order())
    return "".join(parts)
    
  
def build_galaxy_a(is_galaxy_buds, is_galaxy_watch, is_galaxy_a):
    return (
        "👇 Samsung" + "\n" + "\n" +
        format_section('🎧', '<b>Galaxy Buds</b>', is_galaxy_buds) +
        format_section('⌚️', '<b>Galaxy Watch</b>', is_galaxy_watch) +
        format_section('📱', '<b>Galaxy A</b>', is_galaxy_a) +
        build_footer_message_for_order()
    )
    
def build_galaxy_s(is_galaxy_s, is_galaxy_z, is_galaxy_tab):
    return (
        "👇 Samsung" + "\n" + "\n" +
        format_section('📱', '<b>Galaxy S</b>', is_galaxy_s) +
        format_section('📱', '<b>Galaxy Z</b>', is_galaxy_z) +
        format_section('📟', '<b>Galaxy Tab</b>', is_galaxy_tab) +
        build_footer_message_for_order()
    )