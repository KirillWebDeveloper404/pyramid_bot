from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
import datetime

from loader import dp
from sql import User, Tariff, Invest
from keyboards.default import main_kb
from utils import send_invoice, check_pay


@dp.message_handler(text='🧾 Тарифы')
async def tariffs_desc(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    time_now = datetime.datetime.now().hour + float(user.time_zone)
    if time_now < 0:
        time_now -= 24

    text = '1. Тариф минимальный "Start" \n'
    text += '1.5% в день \n'
    text += 'Минимум 5 дней \n'
    text += 'Минимальный порог 300 руб \n'
    text += 'Максимальный порог 300 000 руб \n'
    text += 'Возврат % сразу \n'
    text += 'P.S. Тело депозита по истечению минимального срока'
    text += '\n'
    text += '\n'
    text += '2. Тариф оптимальный "Optimum" \n'
    text += '1.3% в день \n'
    text += 'Минимум 10 дней \n'
    text += 'Минимальный порог 15 300 руб \n'
    text += 'Максимальный порог 1 515 000 руб \n'
    text += 'Возврат % сразу \n'
    text += 'P.S. Тело депозита по истечению минимального срока'
    text += '\n'
    text += '\n'
    text += '3. Тариф максимальный "All" \n'
    text += '1.1% в день \n'
    text += 'Минимум 15 дней \n'
    text += 'Минимальный порог 30 000 руб \n'
    text += 'Максимальный порог 3 000 000 руб \n'
    text += 'Возврат % сразу \n'
    text += 'P.S. Тело депозита по истечению минимального срока'
    text += '\n'
    text += '\n'

    # if 22 <= time_now <= 24:
    if True:
        text += '4. Premium новинка "Night money" \n'
        text += 'Пока ты спишь \n'
        text += '3% за ночь с 24:00 до 06:00 \n'
        text += 'Минимальный порог 50 000 руб \n'
        text += 'Максимальный порог 500 000 руб \n'
        text += 'Возврат тела депозита 7:00 \n'
        text += 'P.S. Тело депозита выплачивается вместе с %'

    await message.answer(text)


