from aiogram import types

# Файл конфигурации клавиатуры
# Конфигурация главной клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_buttons = ["Работа с кредитами", "Запрос в службу поддержки"]
main_keyboard.add(*main_buttons)

# Конфигурация клавиатуры для работы с кредитами
credit_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
credit_buttons = ["Добавить данные о новом кредите", "Рассчитать кредитный пакет в процентах", "Назад"]
credit_keyboard.add(*credit_buttons)

# Конфигурация клавиатуры для выбора типа обращения в службу поддержки
support_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
support_buttons = ["Bug", "New feature", "Other"]
support_keyboard.add(*support_buttons)

# Кнопка отмены для выхода в главное меню в любой момент выполнения программы
cancel_operation = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = ["Отмена"]
cancel_operation.add(*cancel_button)
