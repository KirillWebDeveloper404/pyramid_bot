from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('💲 Инвестиции'), KeyboardButton('👤 Личный кабинет')],
        [KeyboardButton('👔 Реферальная система')],
        [KeyboardButton('📠 Калькулятор')]
    ],
    resize_keyboard=True
)
