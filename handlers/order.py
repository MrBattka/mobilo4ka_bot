from aiogram import Router, types
import asyncio
import json
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import io
from aiogram.exceptions import TelegramRetryAfter

from utils.telegram_loader import sync_suppliers_to_sheets, load_suppliers_config

from utils.keyboards import get_main_menu_kb

from indexPriceFromOrder import (
    processed_list_to_text,
    fetch_and_process_first_sheet,
    fetch_and_process_second_sheet,
    get_fresh_name_used_lists,
    fetch_and_process_seventh_sheet,
    fetch_and_process_sixth_sheet,
    fetch_and_merge_primary_sheets,
    _natural_key
)

from utils.helpers import (
    custom_sort_key_redmi_note,
    custom_sort_key_galaxy_s,
    custom_sort_key_galaxy_a
)

from utils.message_builder import (
    build_footer_message_for_order,
    build_header,
    build_header_for_order,
    build_info_about_price,
    build_info_dyson,
    build_info_price_order,
    build_airpods,
    build_aw,
    build_galaxy_a,
    build_galaxy_s,
    build_game,
    build_garmin,
    build_google,
    build_huawei,
    build_ipad,
    build_iphone_11_15,
    build_iphone_16,
    build_iphone_17,
    build_macbook,
    build_nothing,
    build_poco,
    build_xiaomi
)

from filter_files.apple_filters import (
    is_airpods, is_airpods_max_2, is_airpods_max_2026,
    is_pencil, is_magic, is_apple_tv,
    is_aw_se_2, is_aw_se_3,
    is_aw_s9, is_aw_s10, is_aw_s11,
    is_aw_ul_2, is_aw_ul_3,
    is_ipad_9, is_ipad_10, is_ipad_11,
    is_ipad_mini, is_ipad_air_5, is_ipad_air_11, is_ipad_air_13,
    is_ipad_pro_11, is_ipad_pro_13, is_mac_mini,
    is_imac, is_macbook, is_iphone_11, is_iphone_12, 
    is_iphone_13, is_iphone_14, is_iphone_14_plus, 
    is_iphone_15_eSim, is_iphone_15_1Sim, is_iphone_15_Dual,
    is_iphone_15_plus_eSim, is_iphone_15_plus_1Sim, is_iphone_15_plus_Dual,
    is_iphone_15_pro_eSim, is_iphone_15_pro_1Sim, is_iphone_15_pro_Dual,
    is_iphone_15_pro_max_eSim, is_iphone_15_pro_max_1Sim, is_iphone_15_pro_max_Dual,
    is_iphone_16e_eSim, is_iphone_16e_1Sim, is_iphone_16e_Dual,
    is_iphone_16_eSim, is_iphone_16_1Sim, is_iphone_16_Dual,
    is_iphone_16_plus_eSim, is_iphone_16_plus_1Sim, is_iphone_16_plus_Dual,
    is_iphone_16_pro_eSim, is_iphone_16_pro_1Sim, is_iphone_16_pro_Dual,
    is_iphone_16_pro_max_eSim, is_iphone_16_pro_max_1Sim, is_iphone_16_pro_max_Dual,
    is_iphone_17_e_1Sim, is_iphone_17_e_eSim, is_iphone_17_air, is_iphone_17_e_Dual,
    is_iphone_17_eSim, is_iphone_17_1Sim, is_iphone_17_Dual,
    is_iphone_17_pro_eSim, is_iphone_17_pro_1Sim, is_iphone_17_pro_Dual, 
    is_iphone_17_pro_max_eSim, is_iphone_17_pro_max_1Sim, is_iphone_17_pro_max_Dual
)

from filter_files.samsung_filters import (
    is_galaxy_buds, is_galaxy_a, is_galaxy_s, is_galaxy_z,
    is_galaxy_tab, is_galaxy_watch
)

from filter_files.other_filters import (
    is_dgi, is_gopro, is_jbl, is_marshall, is_beats,
    is_huawei, is_tecno, is_yandex,
    is_pixel_buds, is_pixel_watch, is_pixel_phone, is_pixel_tab,
    is_sony_phone, is_asus, is_realme,
    is_oneplus_buds, is_oneplus_watch, is_oneplus_phone, is_oneplus_tab,
    is_zte, is_nothing_phone, is_nothing_ear, is_honor,
    is_nintendo, is_oculus, is_pico,
    is_playstation, is_xbox, is_steam, is_dualsense,
    is_rayban, is_plaud
)

from filter_files.xiaomi_filters import (
    is_mi_phone, is_mi_pad,
    is_redmi_buds, is_redmi_watch, is_redmi_phone, is_redmi_pad,
    is_poco_phone, is_poco_pad
)

from config.settings import (
    SHEETS_ID_FOR_ORDER,
    CREDENTIALS_FILE,
    CHANNEL_ID_ORDER_PRICE,
    CHANNEL_ID_TEST,
    SUPPLIERS_FILE_ORDER
)

router = Router()

# --- Управление ID сообщений ---
SENT_MESSAGES_FILE = "data/sent_messages_order.json"


def load_message_ids():
    if os.path.exists(SENT_MESSAGES_FILE):
        with open(SENT_MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"main": [], "test": []}


def save_message_ids(data):
    with open(SENT_MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        



@router.message(lambda m: m.text in ["ПРАЙС ПОД ЗАКАЗ", "ПРАЙС ПОД ЗАКАЗ (тест)"])
async def send_order_price(message: types.Message):
    btn = get_main_menu_kb()

    # Определяем режим
    is_main = message.text == "ПРАЙС ПОД ЗАКАЗ"
    chat_id = CHANNEL_ID_ORDER_PRICE if is_main else CHANNEL_ID_TEST
    key = "main" if is_main else "test"

    bot = message.bot

    def truncate_text_to_max_length(text: str, max_len: int = 4090, separator: str = "\n") -> tuple[str, str]:
        """
        Обрезает текст до max_len символов, сохраняя целый последний блок (по последнему separator).
        Возвращает (часть_для_отправки, оставшаяся_часть).
        """
        if len(text) <= max_len:
            return text, ""

        # Ищем последний separator до max_len
        cut_pos = text.rfind(separator, 0, max_len)
        if cut_pos == -1:
            # Если не найден — просто обрезаем
            cut_pos = max_len - len(separator)
        else:
            cut_pos += len(separator)  # Включаем separator в текущую часть

        chunk = text[:cut_pos]
        remaining = text[cut_pos:]
        return chunk, remaining


    async def safe_send_message_with_truncate(chat_id, text, parse_mode='HTML', **kwargs):
        """
        Отправляет текст, обрезая его до 4090 символов, если нужно.
        При необходимости отправляет несколько сообщений по частям.
        """
        max_retries = 5

        while text:
            chunk, remaining = truncate_text_to_max_length(text)
            text = remaining  # подготовим остаток на след. итерацию

            for attempt in range(max_retries):
                try:
                    msg = await bot.send_message(chat_id=chat_id, text=chunk, parse_mode=parse_mode, **kwargs)
                    if not remaining:
                        return msg  # вернём последнее отправленное сообщение
                    # Если есть остаток — продолжаем
                    break  # удачно отправили chunk, переходим к остатку
                except TelegramRetryAfter as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = e.retry_after + 1
                    print(f"[!] Flood control: ждём {wait_time} сек перед отправкой части сообщения (попытка {attempt + 1})")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    print(f"[!] Ошибка при отправке части сообщения: {e}")
                    raise
            else:
                raise RuntimeError("Не удалось отправить часть сообщения после всех попыток")
            await asyncio.sleep(0.1)
    # --- Загружаем и удаляем старые сообщения ---
    all_ids = load_message_ids()
    old_ids = all_ids.get(key, [])
    for msg_id in old_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            pass  # Сообщение могло быть удалено вручную
    all_ids[key] = []  # Очищаем список
    new_message_ids = []

    await message.answer("⏳ Приступил к обновлению прайса под заказ...", parse_mode="Markdown", reply_markup=btn)
    
    await message.answer("📡 Загрузка данных из каналов поставщиков...", parse_mode="Markdown")
    
    suppliers_config = load_suppliers_config(SUPPLIERS_FILE_ORDER)
    if suppliers_config:
        success = await sync_suppliers_to_sheets(suppliers_config, 
                                                 sheet_id=SHEETS_ID_FOR_ORDER,
                                                 suppliers_file=SUPPLIERS_FILE_ORDER)
        if not success:
            await message.answer("❌ Ошибка при обновлении данных из каналов.", parse_mode="Markdown")
            # Можно решить, останавливаться ли здесь или продолжать с тем, что есть
        else:
            await message.answer("✅ Данные из каналов успешно обновлены.", parse_mode="Markdown")
    else:
        await message.answer("ℹ️ Нет конфигурации поставщиков. Пропуск шага загрузки каналов.", parse_mode="Markdown")

    # === Загрузка данных ===
    hi_items = await asyncio.to_thread(fetch_and_process_first_sheet, SHEETS_ID_FOR_ORDER, CREDENTIALS_FILE)
    merged_items, unlinked_items = await asyncio.to_thread(
        fetch_and_merge_primary_sheets, SHEETS_ID_FOR_ORDER, CREDENTIALS_FILE
    )
    garmin_items = await asyncio.to_thread(fetch_and_process_sixth_sheet, SHEETS_ID_FOR_ORDER, CREDENTIALS_FILE)
    dyson_items = await asyncio.to_thread(fetch_and_process_second_sheet, SHEETS_ID_FOR_ORDER, CREDENTIALS_FILE)

    # === Фильтрация по категориям ===
    filtered_iphone_11 = [it for it in hi_items if is_iphone_11(it)]
    filtered_iphone_12 = [it for it in hi_items if is_iphone_12(it)]
    filtered_iphone_13 = [it for it in hi_items if is_iphone_13(it)]
    filtered_iphone_14 = [it for it in hi_items if is_iphone_14(it)]
    filtered_iphone_14_plus = [it for it in hi_items if is_iphone_14_plus(it)]
    filtered_iphone_15_eSim = [it for it in hi_items if is_iphone_15_eSim(it)]
    filtered_iphone_15_1Sim = [it for it in hi_items if is_iphone_15_1Sim(it)]
    filtered_iphone_15_Dual = [it for it in hi_items if is_iphone_15_Dual(it)]
    filtered_iphone_15_plus_eSim = [it for it in hi_items if is_iphone_15_plus_eSim(it)]
    filtered_iphone_15_plus_1Sim = [it for it in hi_items if is_iphone_15_plus_1Sim(it)]
    filtered_iphone_15_plus_Dual = [it for it in hi_items if is_iphone_15_plus_Dual(it)]
    filtered_iphone_15_pro_eSim = [it for it in hi_items if is_iphone_15_pro_eSim(it)]
    filtered_iphone_15_pro_1Sim = [it for it in hi_items if is_iphone_15_pro_1Sim(it)]
    filtered_iphone_15_pro_Dual = [it for it in hi_items if is_iphone_15_pro_Dual(it)]
    filtered_iphone_15_pro_max_eSim = [it for it in hi_items if is_iphone_15_pro_max_eSim(it)]
    filtered_iphone_15_pro_max_1Sim = [it for it in hi_items if is_iphone_15_pro_max_1Sim(it)]
    filtered_iphone_15_pro_max_Dual = [it for it in hi_items if is_iphone_15_pro_max_Dual(it)]

    filtered_iphone_16_eSim = [it for it in hi_items if is_iphone_16_eSim(it)]
    filtered_iphone_16_1Sim = [it for it in hi_items if is_iphone_16_1Sim(it)]
    filtered_iphone_16_Dual = [it for it in hi_items if is_iphone_16_Dual(it)]
    filtered_iphone_16e_eSim = [it for it in hi_items if is_iphone_16e_eSim(it)]
    filtered_iphone_16e_1Sim = [it for it in hi_items if is_iphone_16e_1Sim(it)]
    filtered_iphone_16e_Dual = [it for it in hi_items if is_iphone_16e_Dual(it)]
    filtered_iphone_16_plus_eSim = [it for it in hi_items if is_iphone_16_plus_eSim(it)]
    filtered_iphone_16_plus_1Sim = [it for it in hi_items if is_iphone_16_plus_1Sim(it)]
    filtered_iphone_16_plus_Dual = [it for it in hi_items if is_iphone_16_plus_Dual(it)]
    filtered_iphone_16_pro_eSim = [it for it in hi_items if is_iphone_16_pro_eSim(it)]
    filtered_iphone_16_pro_1Sim = [it for it in hi_items if is_iphone_16_pro_1Sim(it)]
    filtered_iphone_16_pro_Dual = [it for it in hi_items if is_iphone_16_pro_Dual(it)]
    filtered_iphone_16_pro_max_eSim = [it for it in hi_items if is_iphone_16_pro_max_eSim(it)]
    filtered_iphone_16_pro_max_1Sim = [it for it in hi_items if is_iphone_16_pro_max_1Sim(it)]
    filtered_iphone_16_pro_max_Dual = [it for it in hi_items if is_iphone_16_pro_max_Dual(it)]
    filtered_iphone_17e_1Sim = [it for it in hi_items if is_iphone_17_e_1Sim(it)]
    filtered_iphone_17e_eSim = [it for it in hi_items if is_iphone_17_e_eSim(it)]
    filtered_iphone_17e_Dual = [it for it in hi_items if is_iphone_17_e_Dual(it)]
    filtered_iphone_17_eSim = [it for it in hi_items if is_iphone_17_eSim(it)]
    filtered_iphone_17_1Sim = [it for it in hi_items if is_iphone_17_1Sim(it)]
    filtered_iphone_17_Dual = [it for it in hi_items if is_iphone_17_Dual(it)]
    filtered_iphone_17_air = [it for it in hi_items if is_iphone_17_air(it)]
    filtered_iphone_17_pro_eSim = [it for it in hi_items if is_iphone_17_pro_eSim(it)]
    filtered_iphone_17_pro_1Sim = [it for it in hi_items if is_iphone_17_pro_1Sim(it)]
    filtered_iphone_17_pro_Dual = [it for it in hi_items if is_iphone_17_pro_Dual(it)]
    filtered_iphone_17_pro_max_eSim = [it for it in hi_items if is_iphone_17_pro_max_eSim(it)]
    filtered_iphone_17_pro_max_1Sim = [it for it in hi_items if is_iphone_17_pro_max_1Sim(it)]
    filtered_iphone_17_pro_max_Dual = [it for it in hi_items if is_iphone_17_pro_max_Dual(it)]

    filtered_dgi = [it for it in merged_items if is_dgi(it)]
    filtered_gopro = [it for it in merged_items if is_gopro(it)]
    filtered_jbl = [it for it in merged_items if is_jbl(it)]
    filtered_marshall = [it for it in merged_items if is_marshall(it)]
    filtered_beats = [it for it in merged_items if is_beats(it)]
    filtered_plaud = [it for it in merged_items if is_plaud(it)]

    filtered_huawei = [it for it in merged_items if is_huawei(it)]
    filtered_tecno = [it for it in merged_items if is_tecno(it)]
    filtered_yandex = [it for it in merged_items if is_yandex(it)]
    filtered_realme = [it for it in merged_items if is_realme(it)]

    filtered_pixel_buds = [it for it in merged_items if is_pixel_buds(it)]
    filtered_pixel_watch = [it for it in merged_items if is_pixel_watch(it)]
    filtered_pixel_phone = [it for it in merged_items if is_pixel_phone(it)]
    filtered_pixel_tab = [it for it in merged_items if is_pixel_tab(it)]
    filtered_sony = [it for it in merged_items if is_sony_phone(it)]
    filtered_asus = [it for it in merged_items if is_asus(it)]

    filtered_oneplus_buds = [it for it in merged_items if is_oneplus_buds(it)]
    filtered_oneplus_watch = [it for it in merged_items if is_oneplus_watch(it)]
    filtered_oneplus_phone = [it for it in merged_items if is_oneplus_phone(it)]
    filtered_oneplus_tab = [it for it in merged_items if is_oneplus_tab(it)]
    filtered_zte = [it for it in merged_items if is_zte(it)]
    filtered_nothing_phone = [it for it in merged_items if is_nothing_phone(it)]
    filtered_nothing_ear = [it for it in merged_items if is_nothing_ear(it)]
    filtered_honor = [it for it in merged_items if is_honor(it)]

    filtered_galaxy_buds = [it for it in merged_items if is_galaxy_buds(it)]
    filtered_galaxy_watch = [it for it in merged_items if is_galaxy_watch(it)]
    filtered_galaxy_a = sorted([it for it in merged_items if is_galaxy_a(it)], key=custom_sort_key_galaxy_a)
    filtered_galaxy_s = sorted([it for it in merged_items if is_galaxy_s(it)], key=custom_sort_key_galaxy_s)
    filtered_galaxy_z = [it for it in merged_items if is_galaxy_z(it)]
    filtered_galaxy_tab = [it for it in merged_items if is_galaxy_tab(it)]

    filtered_nintendo = [it for it in merged_items if is_nintendo(it)]
    filtered_oculus = [it for it in merged_items if is_oculus(it)]
    filtered_pico = [it for it in merged_items if is_pico(it)]
    filtered_playstation = [it for it in merged_items if is_playstation(it)]
    filtered_dualsense = [it for it in merged_items if is_dualsense(it)]
    filtered_xbox = [it for it in merged_items if is_xbox(it)]
    filtered_steam = [it for it in merged_items if is_steam(it)]
    filtered_rayban = [it for it in merged_items if is_rayban(it)]

    filtered_mi_phone = sorted([it for it in merged_items if is_mi_phone(it)], key=custom_sort_key_redmi_note)
    filtered_mi_pad = [it for it in merged_items if is_mi_pad(it)]
    filtered_redmi_buds = [it for it in merged_items if is_redmi_buds(it)]
    filtered_redmi_watch = [it for it in merged_items if is_redmi_watch(it)]
    filtered_redmi_phone = sorted([it for it in merged_items if is_redmi_phone(it)], key=custom_sort_key_redmi_note)
    filtered_redmi_pad = [it for it in merged_items if is_redmi_pad(it)]

    filtered_poco_phone = [it for it in merged_items if is_poco_phone(it)]
    filtered_poco_pad = [it for it in merged_items if is_poco_pad(it)]

    filtered_airpods = [it for it in hi_items if is_airpods(it)]
    filtered_airpods_max_2 = [it for it in hi_items if is_airpods_max_2(it)]
    filtered_airpods_max_2026 = [it for it in hi_items if is_airpods_max_2026(it)]
    filtered_pencil = [it for it in hi_items if is_pencil(it)]
    filtered_magic = [it for it in hi_items if is_magic(it)]
    filtered_apple_tv = [it for it in hi_items if is_apple_tv(it)]

    filtered_aw_se_2 = [it for it in hi_items if is_aw_se_2(it)]
    filtered_aw_se_3 = [it for it in hi_items if is_aw_se_3(it)]
    filtered_aw_s9 = [it for it in hi_items if is_aw_s9(it)]
    filtered_aw_s10 = [it for it in hi_items if is_aw_s10(it)]
    filtered_aw_s11 = [it for it in hi_items if is_aw_s11(it)]
    filtered_aw_ul_2 = [it for it in hi_items if is_aw_ul_2(it)]
    filtered_aw_ul_3 = [it for it in hi_items if is_aw_ul_3(it)]

    filtered_ipad_9 = [it for it in hi_items if is_ipad_9(it)]
    filtered_ipad_10 = [it for it in hi_items if is_ipad_10(it)]
    filtered_ipad_11 = [it for it in hi_items if is_ipad_11(it)]
    filtered_ipad_mini = [it for it in hi_items if is_ipad_mini(it)]
    filtered_ipad_air_5 = [it for it in hi_items if is_ipad_air_5(it)]
    filtered_ipad_air_11 = [it for it in hi_items if is_ipad_air_11(it)]
    filtered_ipad_air_13 = [it for it in hi_items if is_ipad_air_13(it)]
    filtered_ipad_pro_11 = [it for it in hi_items if is_ipad_pro_11(it)]
    filtered_ipad_pro_13 = [it for it in hi_items if is_ipad_pro_13(it)]

    filtered_mac_mini = [it for it in hi_items if is_mac_mini(it)]
    filtered_imac = [it for it in hi_items if is_imac(it)]
    filtered_macbook = [it for it in hi_items if is_macbook(it)]

    # === Отправка основных блоков ===
    sent_header = await bot.send_message(chat_id=chat_id, text=build_info_price_order(), parse_mode='HTML')
    new_message_ids.append(sent_header.message_id)

    sent_dyson = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text="✂️ Dyson 🪒\n" + processed_list_to_text(dyson_items) +
             build_info_dyson() + "\n" + build_footer_message_for_order(),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_dyson.message_id)
    await asyncio.sleep(0.1)
    sent_garmin = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_garmin(filtered_dgi, garmin_items, filtered_gopro, filtered_jbl, filtered_marshall, filtered_beats,
                          filtered_plaud),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_garmin.message_id)
    await asyncio.sleep(0.1)
    sent_techno = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_huawei(filtered_huawei, filtered_tecno, filtered_yandex, filtered_realme),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_techno.message_id)
    await asyncio.sleep(0.1)
    sent_google = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_google(filtered_pixel_buds, filtered_pixel_watch, filtered_pixel_phone, filtered_pixel_tab,
                          filtered_sony, filtered_asus),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_google.message_id)
    await asyncio.sleep(0.1)
    sent_nothing = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_nothing(filtered_oneplus_buds, filtered_oneplus_watch, filtered_oneplus_phone,
                           filtered_oneplus_tab, filtered_zte, filtered_nothing_phone, filtered_nothing_ear,
                           filtered_honor),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_nothing.message_id)
    await asyncio.sleep(0.1)
    sent_game = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_game(filtered_nintendo, filtered_oculus, filtered_pico, filtered_playstation,
                        filtered_dualsense, filtered_xbox, filtered_steam, filtered_rayban),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_game.message_id)
    await asyncio.sleep(0.1)
    sent_samsung_a = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_galaxy_a(filtered_galaxy_buds, filtered_galaxy_watch, filtered_galaxy_a),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_samsung_a.message_id)
    await asyncio.sleep(0.1)
    sent_samsung_s = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_galaxy_s(filtered_galaxy_s, filtered_galaxy_z, filtered_galaxy_tab),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_samsung_s.message_id)
    await asyncio.sleep(0.1)
    sent_xiaomi = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_xiaomi(filtered_mi_phone, filtered_redmi_buds, filtered_redmi_watch, filtered_redmi_phone),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_xiaomi.message_id)
    await asyncio.sleep(0.1)
    sent_poco = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_poco(filtered_poco_phone, filtered_poco_pad, filtered_mi_pad, filtered_redmi_pad),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_poco.message_id)
    await asyncio.sleep(0.1)
    sent_airpods = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_airpods(filtered_airpods, filtered_airpods_max_2, filtered_airpods_max_2026,
                           filtered_pencil, filtered_magic, filtered_apple_tv),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_airpods.message_id)
    await asyncio.sleep(0.1)
    sent_awatch = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_aw(filtered_aw_se_2, filtered_aw_se_3, filtered_aw_s9, filtered_aw_s10,
                      filtered_aw_s11, filtered_aw_ul_2, filtered_aw_ul_3),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_awatch.message_id)
    await asyncio.sleep(0.1)
    sent_ipad = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_ipad(filtered_ipad_9, filtered_ipad_10, filtered_ipad_11, filtered_ipad_mini,
                        filtered_ipad_air_5, filtered_ipad_air_11, filtered_ipad_air_13,
                        filtered_ipad_pro_11, filtered_ipad_pro_13),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_ipad.message_id)
    await asyncio.sleep(0.1)
    sent_macbook = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_macbook(filtered_mac_mini, filtered_imac, filtered_macbook),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_macbook.message_id)
    await asyncio.sleep(0.1)
    sent_iphone11_15 = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_iphone_11_15(filtered_iphone_11, filtered_iphone_12, filtered_iphone_13,
                                filtered_iphone_14, filtered_iphone_14_plus, 
                                filtered_iphone_15_eSim, filtered_iphone_15_1Sim, filtered_iphone_15_Dual,
                                filtered_iphone_15_plus_eSim, filtered_iphone_15_plus_1Sim, filtered_iphone_15_plus_Dual,
                                filtered_iphone_15_pro_eSim, filtered_iphone_15_pro_1Sim, filtered_iphone_15_pro_Dual,
                                filtered_iphone_15_pro_max_eSim, filtered_iphone_15_pro_max_1Sim, filtered_iphone_15_pro_max_Dual),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_iphone11_15.message_id)
    await asyncio.sleep(0.1)
    sent_iphone_16 = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_iphone_16(filtered_iphone_16e_eSim, filtered_iphone_16e_1Sim, filtered_iphone_16e_Dual,
                             filtered_iphone_16_eSim, filtered_iphone_16_1Sim, filtered_iphone_16_Dual,
                             filtered_iphone_16_pro_eSim, filtered_iphone_16_pro_1Sim, filtered_iphone_16_pro_Dual,
                             filtered_iphone_16_plus_eSim, filtered_iphone_16_plus_1Sim, filtered_iphone_16_plus_Dual,
                             filtered_iphone_16_pro_max_eSim, filtered_iphone_16_pro_max_1Sim, filtered_iphone_16_pro_max_Dual),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_iphone_16.message_id)
    await asyncio.sleep(0.1)
    sent_iphone_17 = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_iphone_17(filtered_iphone_17e_1Sim, filtered_iphone_17e_eSim,
                             filtered_iphone_17e_Dual, filtered_iphone_17_air, 
                             filtered_iphone_17_eSim, filtered_iphone_17_1Sim, filtered_iphone_17_Dual,
                             filtered_iphone_17_pro_eSim, filtered_iphone_17_pro_1Sim, filtered_iphone_17_pro_Dual,
                             filtered_iphone_17_pro_max_eSim, filtered_iphone_17_pro_max_1Sim, filtered_iphone_17_pro_max_Dual,),
        parse_mode='HTML'
    )
    new_message_ids.append(sent_iphone_17.message_id)

    # === Кнопки навигации ===
    base_url = "https://t.me/mobilochka_opt" if is_main else "https://t.me/c/2384328012"

    header = types.InlineKeyboardButton(text="📢 Инфо 📢", url=f"{base_url}/{sent_header.message_id}")
    dyson_btn = types.InlineKeyboardButton(text="🦯 Dyson 🦯", url=f"{base_url}/{sent_dyson.message_id}")
    garmin_btn = types.InlineKeyboardButton(text="⌚️ Garmin ⌚️", url=f"{base_url}/{sent_garmin.message_id}")
    techno_btn = types.InlineKeyboardButton(text="📱 Huawei / Яндекс", url=f"{base_url}/{sent_techno.message_id}")
    google_btn = types.InlineKeyboardButton(text="📱 Google / Sony", url=f"{base_url}/{sent_google.message_id}")
    nothing_btn = types.InlineKeyboardButton(text="📱 Nothing / Honor / OnePlus", url=f"{base_url}/{sent_nothing.message_id}")
    game_btn = types.InlineKeyboardButton(text="🎮 Игровые приставки", url=f"{base_url}/{sent_game.message_id}")
    samsung_a_btn = types.InlineKeyboardButton(text="📱 Samsung A", url=f"{base_url}/{sent_samsung_a.message_id}")
    samsung_s_btn = types.InlineKeyboardButton(text="📱 Samsung S, Z", url=f"{base_url}/{sent_samsung_s.message_id}")
    xiaomi_btn = types.InlineKeyboardButton(text="📱 Xiaomi", url=f"{base_url}/{sent_xiaomi.message_id}")
    poco_btn = types.InlineKeyboardButton(text="📱 Poco", url=f"{base_url}/{sent_poco.message_id}")
    airpods_btn = types.InlineKeyboardButton(text="🎧 AirPods", url=f"{base_url}/{sent_airpods.message_id}")
    awatch_btn = types.InlineKeyboardButton(text="🕦 Apple Watch", url=f"{base_url}/{sent_awatch.message_id}")
    ipad_btn = types.InlineKeyboardButton(text="📟 iPad", url=f"{base_url}/{sent_ipad.message_id}")
    macbook_btn = types.InlineKeyboardButton(text="💻 MacBook / iMac", url=f"{base_url}/{sent_macbook.message_id}")
    iphone11_15_btn = types.InlineKeyboardButton(text="📲 iPhone 11-15 📲", url=f"{base_url}/{sent_iphone11_15.message_id}")
    iphone16_btn = types.InlineKeyboardButton(text="📲 iPhone 16 📲", url=f"{base_url}/{sent_iphone_16.message_id}")
    iphone17_btn = types.InlineKeyboardButton(text="📲 iPhone 17 📲", url=f"{base_url}/{sent_iphone_17.message_id}")
    buy_btn = types.InlineKeyboardButton(text="✍️ Заказать ✍️", url="https://t.me/onlinemyprice")

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [header],
        [dyson_btn],
        [garmin_btn],
        [techno_btn, google_btn],
        [nothing_btn],
        [game_btn],
        [samsung_a_btn, samsung_s_btn],
        [xiaomi_btn, poco_btn],
        [airpods_btn, awatch_btn],
        [ipad_btn, macbook_btn],
        [iphone11_15_btn],
        [iphone16_btn, iphone17_btn],
        [buy_btn]
    ])

    header_msg = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_header_for_order(),
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    new_message_ids.append(header_msg.message_id)
    await asyncio.sleep(0.1)
    info_msg = await safe_send_message_with_truncate(
        chat_id=chat_id,
        text=build_info_about_price(),
        parse_mode='HTML'
    )
    new_message_ids.append(info_msg.message_id)
    await asyncio.sleep(0.1)
    # === ВЫГРУЗКА НЕПРИВЯЗАННЫХ ТОВАРОВ В EXCEL ===
    if unlinked_items:
        wb = Workbook()
        ws = wb.active
        ws.title = "Не привязано к ID"

        headers = ["Название", "Цена", "Причина"]
        ws.append(headers)

        bold = Font(bold=True)
        center = Alignment(horizontal="center", vertical="center")
        for cell in ws[1]:
            cell.font = bold
            cell.alignment = center

        for item in unlinked_items:
            ws.append([
                item["name"],
                item["price"],
                item["reason"]
            ])

        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column].width = adjusted_width

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        document = types.BufferedInputFile(
            file=buffer.getvalue(),
            filename=f"unlinked_items_{key}.xlsx"
        )

        # Отправляем ТОЛЬКО админу в ЛС, НЕ в канал
        ADMIN_ID = 123456789  # ← Замените на ваш ID

        max_retries = 3
        for attempt in range(max_retries):
            try:
                await bot.send_document(
                chat_id=message.from_user.id,
                document=document,
                caption="⚠️ <b>Список позиций, не привязанных к product_id</b>\n\n"
                        f"<i>Режим:</i> <code>{'основной' if is_main else 'тест'}</code>",
                parse_mode='HTML'
                )
                break
            except TelegramRetryAfter as e:
                wait_time = e.retry_after
                print(f"[!] Flood control: ждём {wait_time} секунд перед повтором...")
                await asyncio.sleep(wait_time + 1)
            except Exception as e:
                print(f"[!] Ошибка при отправке Excel админу: {e}")
                try:
                    await message.answer(
                        text="❌ Не удалось отправить Excel-файл с непривязанными товарами.\n"
                             f"Ошибка: <code>{str(e)}</code>",
                        parse_mode='HTML'
                    )
                except:
                    pass  # Если даже сообщение не отправилось — ничего не поделать
                break
    else:
        # Можно тоже уведомить админа, если всё чисто
        try:
            await message.answer(
                text="✅ Все позиции успешно привязаны к ID. Нет непривязанных товаров.",
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"[!] Не удалось отправить уведомление админу: {e}")

    # === Сохранение новых ID ===
    all_ids[key] = new_message_ids
    save_message_ids(all_ids)

    await message.answer("✅ Прайс успешно обновлён", parse_mode='Markdown', reply_markup=btn)