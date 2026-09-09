import json
from aiogram import Router, types
from indexPriceFromOrder import get_fresh_name_used_lists
from utils.message_builder import build_header
from config.settings import CHANNEL_ID, CHANNEL_ID_TEST
from category import getApple, getUsed, getSamsung, getXiaomiYandexJBL, getCoros
from utils.keyboards import get_main_menu_kb
from aiogram.filters import Command

router = Router()

# Путь к JSON-файлу
SENT_MESSAGES_FILE = "data/sent_messages.json"

# Загружаем все message_id
def load_all_message_ids():
    try:
        with open(SENT_MESSAGES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "main": data.get("main", []),
                "test": data.get("test", [])
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"main": [], "test": []}

# Сохраняем все message_id
def save_all_message_ids(data: dict):
    with open(SENT_MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = get_main_menu_kb()
    await message.answer(
        "👋 Привет! Я бот Mobilo4ka.\n\n"
        "Выбери нужное действие в меню ниже:", 
        reply_markup=kb
    )

@router.message(lambda m: m.text in ["ПРАЙС ПО НАЛИЧИЮ", "ПРАЙС ПО НАЛИЧИЮ (тест)"])
async def send_stock_price(message: types.Message):
    name_list, used_list = await get_fresh_name_used_lists()
    btn = get_main_menu_kb()
    header = build_header()

    bot = message.bot
    is_main = message.text == "ПРАЙС ПО НАЛИЧИЮ"
    chat_id = CHANNEL_ID if is_main else CHANNEL_ID_TEST
    key = "main" if is_main else "test"

    # Загружаем ВСЕ ID
    all_ids = load_all_message_ids()
    old_message_ids = all_ids[key]

    # Удаляем старые сообщения из нужного канала
    for msg_id in old_message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            print(f"🗑 Удалено сообщение {msg_id} из {key}-канала")
        except Exception as e:
            print(f"❌ Не удалось удалить {msg_id}: {e}")

    # Отправляем новые сообщения
    new_message_ids = []
    messages_to_send = [
        (header, "Markdown"),
        (getApple(name_list), "Markdown"),
        (getSamsung(name_list), "Markdown"),
        (getCoros(name_list), "Markdown"),
        (getXiaomiYandexJBL(name_list), "Markdown"),
        (getUsed(used_list), "HTML"),
    ]
    
    await message.answer("⏳Приступил к обновлению прайса по наличию...", parse_mode="Markdown", reply_markup=btn)

    for text, parse_mode in messages_to_send:
        sent_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode
        )
        new_message_ids.append(sent_message.message_id)

    # Обновляем только нужную часть
    all_ids[key] = new_message_ids
    save_all_message_ids(all_ids)

    # Подтверждение
    status = "основной" if is_main else "тестовый"
    await message.answer(f"Цены успешно отправлены в {status} канал.", reply_markup=btn)