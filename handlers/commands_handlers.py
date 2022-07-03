from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config.keyboard import main_keyboard, credit_keyboard
from database.insert_methods import add_user
from database.select_methods import check_user
from main import dp


@dp.message_handler(commands=['start'], state="*")
async def welcome(message: types.Message):
    print("Starting welcome script")
    user_exist = check_user(message.from_user.id)

    if user_exist:
        await message.answer(f"Снова здравствуйте, {message.from_user.full_name}")
        await message.answer("Дальнейшие варианты действия представлены в клавиатуре",
                             reply_markup=main_keyboard)

    else:
        user_added = add_user(message.from_user.id)
        if user_added:
            await message.answer("Здравствуйте, {message.from_user.username}")
            await message.answer("Дальнейшие варианты действия представлены в клавиатуре",
                                 reply_markup=main_keyboard)
        else:
            await message.answer("Ошибка при добавлении")


@dp.message_handler(Text(equals="Работа с кредитами"))
async def credit_menu(message: types.Message):
    await message.answer("В меню представлены варианты действий для работы с кредитами",
                         reply_markup=credit_keyboard)


@dp.message_handler(Text(equals="Назад"))
async def back_to_start(message: types.Message):
    await message.answer("Вы возвращены в главное меню",
                         reply_markup=main_keyboard)


@dp.message_handler(Text(equals="Отмена"), state="*")
async def reject(message: types.Message, state: FSMContext):
    await message.answer("Действия отменены, возврат в главное меню",
                         reply_markup=main_keyboard)
    await state.finish()
