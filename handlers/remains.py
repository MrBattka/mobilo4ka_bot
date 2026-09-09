from aiogram import Router, types
from refreshPriceRemains import process_sheet
from config.settings import SHEETS_ID_REMAINS, CREDENTIALS_FILE
import asyncio
from utils.keyboards import get_main_menu_kb

router = Router()

@router.message(lambda m: m.text == 'ПРОСТАВИТЬ ЦЕНЫ В ОСТАТКАХ')
async def send_stock_price(message: types.Message):
    # ✅ Правильное получение данных

    btn = get_main_menu_kb()

    if message.text == 'ПРОСТАВИТЬ ЦЕНЫ В ОСТАТКАХ':
        
        updates, applied = await asyncio.to_thread(
            process_sheet,
            sheet_key=SHEETS_ID_REMAINS,
            credentials_file=CREDENTIALS_FILE,
            apply=False
        )
        await message.answer(f"Планируемые обновления: {len(updates)}", reply_markup=btn)

        updates, applied = await asyncio.to_thread(
            process_sheet,
            sheet_key=SHEETS_ID_REMAINS,
            credentials_file=CREDENTIALS_FILE,
            apply=True
        )
        await message.answer(f"Применено: {applied}", reply_markup=btn)