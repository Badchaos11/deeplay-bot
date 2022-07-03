from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from database.select_methods import get_all_credits
from config.keyboard import main_keyboard


@dp.message_handler(Text(equals="Рассчитать кредитный пакет в процентах"))
async def all_credits(message: types.Message):
    print(f"Начинаю получать данные о кредитах пользователя {message.from_user.id}")
    credit_data = get_all_credits(message.from_user.id)

    final_sum = 0
    if len(credit_data) == 0:
        await message.answer("В настоящий момент кредитов нет")
    for credit in credit_data:
        final_sum += credit['size']
    for credit in credit_data:
        await message.answer(f"В банке {credit['bank']} содержится "
                             f"{round((credit['size'] / final_sum) * 100, 3)}% "
                             f"от общей задолженности.",
                             reply_markup=main_keyboard)
