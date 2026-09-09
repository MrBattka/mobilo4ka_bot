from aiogram import Router, types
import logging
from utils.keyboards import get_main_menu_kb
from utils.gsheet_updater import update_column_g_in_sheet_async
from config.settings import CREDENTIALS_FILE, SHEETS_ID_FOR_ORDER

router = Router()
logger = logging.getLogger(__name__)

@router.message(lambda m: m.text == "ОБНОВИТЬ ЦЕНЫ ОПТ")
async def refresh_stock_price(message: types.Message):
    btn = get_main_menu_kb()
    await message.answer("⏳ Приступил к обновлению цен по наличию...", reply_markup=btn, parse_mode="HTML")

    try:
        result_message = await update_column_g_in_sheet_async(
            credentials_file=CREDENTIALS_FILE,
            spreadsheet_url=f'https://docs.google.com/spreadsheets/d/{SHEETS_ID_FOR_ORDER}'
        )
    except Exception as e:
        logger.exception("Ошибка при обновлении цен")  # Полный traceback
        result_message = f"❌ Произошла ошибка: {type(e).__name__}: {e}"

    if len(result_message) <= 4096:
        await message.answer(result_message, reply_markup=btn, parse_mode="HTML")
    else:
        # Делим на части по 4096 символов
        parts = []
        while len(result_message) > 4096:
            # Находим последнее место для разрыва — перед концом строки
            cut_index = result_message.rfind('\n', 0, 4096)
            if cut_index == -1:
                cut_index = 4096  # аварийный разрыв
            parts.append(result_message[:cut_index])
            result_message = result_message[cut_index:].lstrip()
        parts.append(result_message)

        # Отправляем по частям
        for i, part in enumerate(parts):
            # Кнопки только в последнем сообщении
            keyboard = btn if i == len(parts) - 1 else None
            await message.answer(part, reply_markup=keyboard, parse_mode="HTML")