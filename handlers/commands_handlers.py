from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config.keyboard import main_keyboard, credit_keyboard
from database.insert_methods import add_user
from database.select_methods import check_user
from main import dp

# Хэндлеры команд и общие хэндлеры, предназначенные для переходов по пунктам меню


@dp.message_handler(commands=['start'], state="*")
async def welcome(message: types.Message):  # Функция для начала работы с ботом.
    print("Starting welcome script")
    user_exist = check_user(message.from_user.id)  # Проверяется наличие пользователя в базе данных.

    if user_exist:  # Ветвь - если пользователь уже добавлен в базу
        await message.answer(f"Снова здравствуйте, {message.from_user.full_name}")  # Приветствие
        await message.answer("Дальнейшие варианты действия представлены в клавиатуре",  # Переход в меню
                             reply_markup=main_keyboard)  # Изменение клавиатуры

    else:  # етвь добавления нового пользователя
        user_added = add_user(message.from_user.id)  # Добавление пользователя в базу
        if user_added:  # При успехе добавления
            await message.answer(f"Здравствуйте, {message.from_user.full_name}")  # Приветствие
            await message.answer("Дальнейшие варианты действия представлены в клавиатуре",  # Сообщение и переход к меню
                                 reply_markup=main_keyboard)  # Изменение клавиатуры
        else:
            await message.answer("Ошибка при добавлении")  # Сообщение при ошибке добавления пользователя


@dp.message_handler(Text(equals="Работа с кредитами"))  # Переход в подменю работы с кредитами
async def credit_menu(message: types.Message):
    await message.answer("В меню представлены варианты действий для работы с кредитами",  # ообщение о переходе
                         reply_markup=credit_keyboard)  # Изменение кнопок меню


@dp.message_handler(Text(equals="Назад"))  # Возвращение в главное меню
async def back_to_start(message: types.Message):
    await message.answer("Вы возвращены в главное меню",  # Сообщение о переходе
                         reply_markup=main_keyboard)  # Изменение меню


@dp.message_handler(Text(equals="Отмена"), state="*")   # Отмена текущей цепочки действий
async def reject(message: types.Message, state: FSMContext):
    await message.answer("Действия отменены, возврат в главное меню",  # Сообщение о переходе
                         reply_markup=main_keyboard)  # Изменение меню
    await state.finish()  # Сброс состояний и запомненных действий, если они были
