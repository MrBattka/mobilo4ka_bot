import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher

from config.settings import BOT_TOKEN

from handlers import base, order, remains, refreshPrice, parsingPricesForWebsite

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

async def main():
    dp.include_router(base.router)
    dp.include_router(order.router)
    dp.include_router(remains.router)
    dp.include_router(refreshPrice.router)
    dp.include_router(parsingPricesForWebsite.router)
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())