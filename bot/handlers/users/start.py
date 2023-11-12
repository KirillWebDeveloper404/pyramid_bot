from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
import datetime

from loader import dp
from sql import User
from keyboards.default import main_kb


@dp.message_handler(CommandStart(), state='*')
@dp.message_handler(text='Главное меню', state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        user = User.get(User.tg_id == message.from_user.id)
        rep_kb = await message.answer("Бот инвестиции",
                             reply_markup=main_kb)
        await rep_kb.delete()
        await message.answer("Бот инвестиции",
                             reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                 InlineKeyboardButton(text='⚙️ Поддержка', url='https://t.me/FairMoney2023'),
                                 InlineKeyboardButton(text='⚙️ Поддержка(запасная ссылка)', url='https://t.me/FairMoney23')
                             ))

    except User.DoesNotExist:
        user = User()
        user.tg_id = message.from_user.id

        if len(message.text.split(' ')) == 2:
            user.referal = message.text.split(' ')[1]

        user.save()
        await message.answer("Сколько сейчас у тебя времени? \nНапиши только час, число от 0 до 24")
        await state.set_state('set_time')


@dp.message_handler(state='set_time')
async def set_time(message: types.Message, state: FSMContext):
    try:
        user = User.get(User.tg_id == message.from_user.id)

        try:
            if 0 <= int(message.text) <= 24:
                user.time_zone = int(message.text) - int(datetime.datetime.now().strftime('%H'))
                user.save()
                await bot_start(message, state)
            else:
                await message.answer("Пришлите только час, число от 0 до 24")
                return
        except:
            await message.answer("Пришлите только час, число от 0 до 24")
            return

    except User.DoesNotExist:
        await bot_start(message, state)
