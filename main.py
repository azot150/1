from loguru import logger
import time
import re

logger.add("log/file.log", format="{time} {level} {message}", level="DEBUG", rotation="1 week", compression="zip")

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, admin_id

token = TOKEN
admin_id = admin_id

bot = Bot(token=token)
dp = Dispatcher(bot)


if __name__ == '__main__':
    from handlers import dp, send_to_admin
    logger.info("Bot authorization successful")
    executor.start_polling(dp, skip_updates=True, on_startup=send_to_admin)
