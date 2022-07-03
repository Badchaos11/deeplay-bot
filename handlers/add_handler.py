from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.keyboard import cancel_operation, main_keyboard
from database.insert_methods import add_credit
from database.select_methods import check_credit_in_bank, get_credit_data
from database.update_methods import update_credit
from loader import dp


class NewCredit(StatesGroup):
    waiting_for_credit_bank = State()
    waiting_for_credit_size = State()


@dp.message_handler(Text(equals="Добавить данные о новом кредите"))
async def new_credit_start(message: types.Message):
    await message.answer("Введите название банка, в котором хотите взять кредит.",
                         reply_markup=cancel_operation)
    await NewCredit.waiting_for_credit_bank.set()


@dp.message_handler(state=NewCredit.waiting_for_credit_bank)
async def new_credit_size(message: types.Message, state: FSMContext):
    if len(message.text) == 0:
        await message.answer("Введите корректное название банка")
        return
    await state.update_data(bank_name=message.text)

    await NewCredit.next()
    await message.answer("Введите размер кредита.",
                         reply_markup=cancel_operation)


@dp.message_handler(state=NewCredit.waiting_for_credit_size)
async def new_credit_add_final(message: types.Message, state: FSMContext):
    if len(message.text) == 0:
        await message.answer("Введите корректную сумму кредита")
        return
    elif int(message.text) < 0:
        await message.answer("Введите корректную сумму кредита",
                             reply_markup=cancel_operation)
        return

    bank_data = await state.get_data()

    credit_in_bank = check_credit_in_bank(message.from_user.id, bank_data['bank_name'])

    if credit_in_bank:
        old_size = get_credit_data(message.from_user.id, bank_data['bank_name'])
        new_size = float(message.text) + old_size
        update = update_credit(message.from_user.id, new_size, bank_data['bank_name'])
        if update:
            await message.answer(f"Кредит в банке {bank_data['bank_name']} успешно обновлен",
                                 reply_markup=main_keyboard)
        else:
            await message.answer("Что-то пошло не так при обновлении")
    else:
        transaction = add_credit(message.from_user.id, float(message.text), bank_data['bank_name'])

        if transaction:
            await message.answer("Кредит успешно выдан.",
                                 reply_markup=main_keyboard)
        else:
            await message.answer("Ошибка. Кредит не был выдан")
    await state.finish()
