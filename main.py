import logging

from aiogram.utils import executor
from handlers import dp

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Старт бота
if __name__ == "__main__":
    print("Bot has been started")
    executor.start_polling(dp, skip_updates=False)
