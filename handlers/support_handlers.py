import json
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.keyboard import support_keyboard, main_keyboard
from loader import dp, bot


class SupportTicket(StatesGroup):
    waiting_for_ticket_type = State()
    waiting_for_ticket_description = State()
    waiting_for_ticket_image = State()


available_ticket_types = ["Bug", "New feature", "Other"]


@dp.message_handler(Text(equals="Запрос в службу поддержки"))
async def support_ticket_start(message: types.Message):
    await message.answer("Выберите один из доступных вариантов для запроса в службу поддержки",
                         reply_markup=support_keyboard)
    await SupportTicket.waiting_for_ticket_type.set()


@dp.message_handler(state=SupportTicket.waiting_for_ticket_type)
async def support_ticket_describe(message: types.Message, state: FSMContext):
    print("Получен тип")
    if message.text not in available_ticket_types:
        await message.answer("Пожалуйста, выберите тип запроса из представленных")
        return
    await state.update_data(ticket_type=message.text)

    await SupportTicket.next()
    await message.answer("Введите описание проблемы")


@dp.message_handler(state=SupportTicket.waiting_for_ticket_description)
async def support_ticket_load_image(message: types.Message, state: FSMContext):
    print("Получено описание")
    if len(message.text) == 0:
        await message.answer("Пожалуйста, введите описание проблемы")
        return
    await state.update_data(ticket_description=message.text)

    await SupportTicket.next()
    await message.answer("Загрузите изображение, показывающее вашу проблему")


@dp.message_handler(state=SupportTicket.waiting_for_ticket_image, content_types=["photo"])
async def support_ticket_finish(message: types.Message, state: FSMContext):
    print("Получено всё")

    ticket_data = await state.get_data()
    ticket_type = ticket_data['ticket_type']
    ticket_description = ticket_data['ticket_description']
    ticket_image = await bot.get_file(message.photo[-1].file_id)
    print(ticket_image)
    file_path = ticket_image.file_path

    print(file_path)
    await message.photo[-1].download(f"tickets/images/{ticket_image['file_unique_id']}.jpg")

    data = {"ticket": {
        'type': ticket_type,
        'description': ticket_description,
        'image': f"tickets/images/{ticket_image}"
    }}

    with open(f"tickets/ticket-{message.from_user.id}", "w") as result_file:
        json.dump(data, result_file)

    await state.finish()
    await message.answer("Обращение в службу поддержки успешно создано.",
                         reply_markup=main_keyboard)


