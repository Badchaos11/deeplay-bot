import json
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.keyboard import support_keyboard, main_keyboard, cancel_operation
from loader import dp, bot


# Машина конечных состояний для создания запроса в службу поддержки
class SupportTicket(StatesGroup):
    waiting_for_ticket_type = State()
    waiting_for_ticket_description = State()
    waiting_for_ticket_image = State()


available_ticket_types = ["Bug", "New feature", "Other"]


@dp.message_handler(Text(equals="Запрос в службу поддержки"))  # Инициализация запроса
async def support_ticket_start(message: types.Message):
    await message.answer("Выберите один из доступных вариантов для запроса в службу поддержки",  # Доступные темы
                         reply_markup=support_keyboard)
    await SupportTicket.waiting_for_ticket_type.set()  # Изменение состояния FSM


@dp.message_handler(state=SupportTicket.waiting_for_ticket_type)  # Вторая функция в цепочке
async def support_ticket_describe(message: types.Message, state: FSMContext):
    print("Получен тип")
    if message.text not in available_ticket_types:  # Проверка на правильность темы
        await message.answer("Пожалуйста, выберите тип запроса из представленных")
        return
    await state.update_data(ticket_type=message.text)  # Сохранение темы запроса в память

    await SupportTicket.next()  # Изменение сосотяния
    await message.answer("Введите описание проблемы",
                         reply_markup=cancel_operation)


@dp.message_handler(state=SupportTicket.waiting_for_ticket_description)  # Третья функция в цепочке
async def support_ticket_load_image(message: types.Message, state: FSMContext):
    print("Получено описание")
    if len(message.text) == 0:  # Проверка на ввод
        await message.answer("Пожалуйста, введите описание проблемы")
        return
    await state.update_data(ticket_description=message.text)  # Сохранения описания в память

    await SupportTicket.next()  # Изменение состояния
    await message.answer("Загрузите изображение, показывающее вашу проблему",
                         reply_markup=cancel_operation)


@dp.message_handler(state=SupportTicket.waiting_for_ticket_image, content_types=["photo"])  # Завершение цепочки
async def support_ticket_finish(message: types.Message, state: FSMContext):
    print("Получено всё")

    ticket_data = await state.get_data()  # Получение данных из хранилища
    ticket_type = ticket_data['ticket_type']  # Создание переменных для удобства кода
    ticket_description = ticket_data['ticket_description']  # Из памяти получены тема и описание запроса
    ticket_image = await bot.get_file(message.photo[-1].file_id)  # Получение информации об загруженном изображении
    file_path = ticket_image.file_path

    print(file_path)
    await message.photo[-1].download(f"tickets/images/{ticket_image['file_unique_id']}.jpg")  # Сохранение изображения

    # Создание структуры JSON-документа
    data = {"ticket": {
        'type': ticket_type,
        'description': ticket_description,
        'image': f"tickets/images/{ticket_image['file_unique_id']}.jpg"
    }}

    # Сохранение запроса
    with open(f"tickets/ticket-{message.from_user.id}-{datetime.now()}", "w") as result_file:
        json.dump(data, result_file)

    await state.finish()  # Сброс состояний и очистка хранилища
    await message.answer("Обращение в службу поддержки успешно создано.",
                         reply_markup=main_keyboard)  # Переход в главное меню
