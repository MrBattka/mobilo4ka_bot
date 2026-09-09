from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_kb() -> ReplyKeyboardMarkup:
    
    # Возвращает основную клавиатуру бота
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='ПРАЙС ПО НАЛИЧИЮ'),
                KeyboardButton(text='ПРАЙС ПО НАЛИЧИЮ (тест)')
            ],
            [
                KeyboardButton(text='ПРАЙС ПОД ЗАКАЗ'),
                KeyboardButton(text='ПРАЙС ПОД ЗАКАЗ (тест)')
            ],
            [
                KeyboardButton(text='ОБНОВИТЬ ЦЕНЫ ОПТ'),
                KeyboardButton(text='ПРОСТАВИТЬ ЦЕНЫ В ОСТАТКАХ')
            ],
            [
                KeyboardButton(text='ВЫГРУЗКА ПОСТАВЩИКОВ')
            ]
        ],
        resize_keyboard=True
    )