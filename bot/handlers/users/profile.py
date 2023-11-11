from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
import datetime

from loader import dp
from sql import User, Invest
from keyboards.default import main_kb


@dp.message_handler(text='👤 Личный кабинет')
async def profile(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    text = f'👤 Личный кабинет: \n\n'
    text += f'Ваш ID: {message.from_user.id} \n'
    text += f'Баланс: {user.balance} ₽'

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text='Мои тарифы', callback_data='tariff'))
    kb.add(InlineKeyboardButton(text='Пополнить', callback_data='add_balance'),
           InlineKeyboardButton(text='Вывести', callback_data='money_out'))

    del_kb = await message.answer('loading', reply_markup=ReplyKeyboardRemove())
    await del_kb.delete()

    await message.answer(text, reply_markup=kb)


@dp.callback_query_handler(text='tariff')
async def my_tariff(c: types.CallbackQuery, state: FSMContext):
    user = User.get(User.tg_id == c.from_user.id)
    tariffs_ = Invest.select().where(Invest.user == user.id)
    tariffs = [el for el in tariffs_]

    if len(tariffs) == 0:
        await c.message.answer("Вы пока что не оплатили ни одного тарифа, найти их можно во вкладке Инвестиции")
    else:
        await c.message.answer("Ваши тарифы:",
                               reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Главное меню")]], resize_keyboard=True))
    for tariff in tariffs:
        text = tariff.get_info()
        try:
            if datetime.datetime.now() >= datetime.datetime.strptime(tariff.apply_out, '%d.%m.%Y'):
                kb = InlineKeyboardMarkup()
                kb.add(InlineKeyboardButton(text='Снять проценты', callback_data=f'{tariff.id}'))
                await c.message.answer(text, reply_markup=kb)
            else:
                await c.message.answer(text)
        except:
            await c.message.answer(text)
    else:
        await state.set_state('percent_out')


@dp.callback_query_handler(state='percent_out')
async def percent_out(c: types.CallbackQuery, state: FSMContext):
    user = User.get(User.tg_id == c.from_user.id)
    tariff = Invest.get(Invest.id == c.data)
    percent = tariff.sum.split(' ')[1]

    tariff.sum = f'{float(tariff.sum.split(" ")[0])} 0'
    tariff.save()

    user.balance = float(user.balance) + float(percent)
    user.save()

    await c.message.answer(f"{percent}p успешно переведены на ваш баланс.\n"
                           "Вы можете снять деньги в разделе Личный кабинет -> Вывести",
                           reply_markup=main_kb
                           )
    await state.finish()
