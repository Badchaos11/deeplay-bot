from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Загрузка параметров, необходимых для бота - токен бота
load_dotenv()
# Создание объектов бота - диспетчер и сам бот
bot = Bot(str(os.getenv("BOT_TOKEN")))
dp = Dispatcher(bot, storage=MemoryStorage())
