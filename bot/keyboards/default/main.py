from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('👤 Личный кабинет'), KeyboardButton('📠 Калькулятор')],
        [KeyboardButton('🧾 Тарифы'), KeyboardButton('💲 Инвестировать')],
        [KeyboardButton('👔 Реферальная система')]
    ],
    resize_keyboard=True
)
