from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from database.select_methods import get_all_credits
from config.keyboard import main_keyboard


# Обработчики сообщений с методами, не изменяющими базу данных


@dp.message_handler(Text(equals="Рассчитать кредитный пакет в процентах"))  # Функция обработки расчёта процентов
async def all_credits(message: types.Message):
    print(f"Начинаю получать данные о кредитах пользователя {message.from_user.id}")  # Сообщение о начале работы
    credit_data = get_all_credits(message.from_user.id)  # Запрос в базу данных по userid

    final_sum = 0  # переменная для хранения общей суммы кредитов
    if len(credit_data) == 0:
        await message.answer("В настоящий момент кредитов нет")  # Проверка на наличие кредитов.
    for credit in credit_data:
        final_sum += credit['size']  # Суммирование всех кредитов
    for credit in credit_data:
        await message.answer(f"В банке {credit['bank']} содержится "  # Вывод результата
                             f"{round((credit['size'] / final_sum) * 100, 3)}% "  # Процент по каждому кредиту  
                             f"от общей задолженности.",
                             reply_markup=main_keyboard)  # Изменение клавиатуры на главную
