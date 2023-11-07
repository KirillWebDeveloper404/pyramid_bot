from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from sql import User


@dp.message_handler(CommandStart(), state='*')
@dp.message_handler(text='Главное меню', state='*')
async def bot_start(message: types.Message):
    try:
        user = User.get(User.tg_id == message.from_user.id)
    except User.DoesNotExist:
        user = User()
        user.tg_id = message.from_user.id
        user.save()

    await message.answer("Привет")
