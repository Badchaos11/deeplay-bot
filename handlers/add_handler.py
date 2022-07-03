from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.keyboard import cancel_operation, main_keyboard
from database.insert_methods import add_credit
from database.select_methods import check_credit_in_bank, get_credit_data
from database.update_methods import update_credit
from loader import dp


#  Машина конечных состояний для создания нового кредита
class NewCredit(StatesGroup):
    waiting_for_credit_bank = State()
    waiting_for_credit_size = State()


# Обработчики сообщений для добавления в базу данных новых кредитов


@dp.message_handler(Text(equals="Добавить данные о новом кредите"))  # Первое сообщение в цепочке
async def new_credit_start(message: types.Message):
    await message.answer("Введите название банка, в котором хотите взять кредит.",  # Запрос на ввод сообщения
                         reply_markup=cancel_operation)
    await NewCredit.waiting_for_credit_bank.set()  # Изменения состояния FSM


@dp.message_handler(state=NewCredit.waiting_for_credit_bank)
async def new_credit_size(message: types.Message, state: FSMContext):  # Второе сообщение в цепочке
    if len(message.text) == 0:  # Проверка на то, что сообщение введено
        await message.answer("Введите корректное название банка")
        return
    await state.update_data(bank_name=message.text)  # Запись данных во временную память бота

    await NewCredit.next()  # Включение следующего состояния FSM
    await message.answer("Введите размер кредита.",  # Запрос на  ввод
                         reply_markup=cancel_operation)


@dp.message_handler(state=NewCredit.waiting_for_credit_size)
async def new_credit_add_final(message: types.Message, state: FSMContext):  # Последняя функция в цепочке
    if len(message.text) == 0:
        await message.answer("Введите корректную сумму кредита")
        return
    elif int(message.text) < 0:  # Проверка на знак числа
        await message.answer("Введите корректную сумму кредита",
                             reply_markup=cancel_operation)
        return

    bank_data = await state.get_data()  # Получение данных из хранилища

    credit_in_bank = check_credit_in_bank(message.from_user.id, bank_data['bank_name'])  # Проверка на наличие
                                                                                         # кредита в банке
    if credit_in_bank:  # Если кредит есть
        old_size = get_credit_data(message.from_user.id, bank_data['bank_name'])  # Получение суммы староко кредита
        new_size = float(message.text) + old_size  # Обновление суммы
        update = update_credit(message.from_user.id, new_size, bank_data['bank_name'])  # Запись в базу данных
        if update:  # Проверка на результат транзакции
            await message.answer(f"Кредит в банке {bank_data['bank_name']} успешно обновлен",  # Успех
                                 reply_markup=main_keyboard)
        else:
            await message.answer("Что-то пошло не так при обновлении",  # Неудача
                                 reply_markup=main_keyboard)
    else:  # Если кредита в данном банке нет
        transaction = add_credit(message.from_user.id, float(message.text), bank_data['bank_name'])  # Добавление нового кредита

        if transaction:  # Проверка на результат транзакции
            await message.answer("Кредит успешно выдан.",  # Успех
                                 reply_markup=main_keyboard)
        else:
            await message.answer("Ошибка. Кредит не был выдан",  # Неудача
                                 reply_markup=main_keyboard)
    await state.finish()  # Сброс всех состояний, удаление данных из памяти
