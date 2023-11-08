from aiogram import types

from loader import dp
from sql import User


@dp.message_handler(text='👔 Реферальная система')
async def ref(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    refs = User.select(User.referal == user.tg_id)

    text = f"▪️ Вас пригласил: {user.referal if user.referal else 'никто'}\n"
    text += f"▪️ Партнеров: {len(refs)-1} чел \n\n"
    text += "🌐 Ваша реферальная ссылка:\n"
    text += f"https://t.me/TestPyTeIegramBot?start={user.tg_id}"
    await message.answer(text)
