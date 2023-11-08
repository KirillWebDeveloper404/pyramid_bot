from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
import datetime

from loader import dp
from sql import User, Tariff, Invest
from keyboards.default import main_kb


@dp.message_handler(text='💲 Инвестиции')
@dp.message_handler(text='Назад', state='select_tariff')
@dp.message_handler(text='Назад', state='buy_tariff')
async def list_tariff(message: types.Message, state: FSMContext):
    tariffs = Tariff().select()
    tariffs_list = [el for el in tariffs]
    kb = InlineKeyboardMarkup(row_width=1)

    for el in tariffs_list:
        kb.add(InlineKeyboardButton(text=el.name, callback_data=el.id))

    del_kb = await message.answer('loading', reply_markup=ReplyKeyboardRemove())
    await del_kb.delete()

    await message.answer("Наша платформа предлагает выгодно в кратчайшие сроки приумножить ваши средства.",
                         reply_markup=kb)
    await state.set_state('select_tariff')


@dp.callback_query_handler(state='select_tariff')
async def select_tariff(c: types.CallbackQuery, state: FSMContext):
    tariff = Tariff.get(Tariff.id == int(c.data))
    kb = ReplyKeyboardMarkup(
        [
            [KeyboardButton('Купить этот тариф')],
            [KeyboardButton('Назад')],
        ],
        resize_keyboard=True
    )
    text = tariff.get_info()

    await c.message.answer(
        text=text,
        reply_markup=kb
    )
    await state.set_data({'tariff': tariff})
    await state.set_state('select_tariff')


@dp.message_handler(text='Купить этот тариф', state='select_tariff')
async def buy_tariff(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await message.answer('Какую сумму вы хотите вложить?\nВведите только число', reply_markup=ReplyKeyboardRemove())
    await state.set_data(data)
    await state.set_state('select_sum')


@dp.message_handler(state='select_sum')
async def select_sum(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        data['sum'] = int(message.text)
        tariff = data['tariff']
        user = User.get(User.tg_id == message.from_user.id)

        if int(tariff.maximum) < int(message.text) < int(tariff.minimum):
            await message.answer("Ввыдете сумму в пределах лимита")
            await state.set_data(data)
            await state.set_state('select_sum')
            return
        if int(user.balance) < int(message.text):
            await message.answer("У вас на балансе недостаточно средств")
            await state.set_data(data)
            await state.set_state('select_sum')
            return

        kb = ReplyKeyboardMarkup(
            [
                [KeyboardButton('Оплатить')],
                [KeyboardButton('Назад')],
            ],
            resize_keyboard=True
        )
        text = tariff.get_info(buy=True, summ=int(message.text))

        await message.answer(text=text, reply_markup=kb)
        await state.set_data(data)
        await state.set_state('buy_tariff')

    except:
        await message.answer('Неверно введена сумма. Введите только число')
        await state.set_data(data)
        await state.set_state('select_sum')


@dp.message_handler(text='Оплатить', state='buy_tariff')
async def buy_tariff(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tariff = data['tariff']
    user = User.get(User.tg_id == message.from_user.id)

    user.balance = int(user.balance) - data['sum']
    user.save()

    invest = Invest()
    invest.name = tariff.name
    invest.user = user.id
    invest.sum = f'{data["sum"]} 0'
    if tariff.start_time == '-1':
        invest.deadline = (datetime.datetime.now() + datetime.timedelta(days=int(tariff.end_time))).strftime('%d.%m.%Y')
        invest.apply_out = (datetime.datetime.now() + datetime.timedelta(days=int(tariff.deadline))).strftime('%d.%m.%Y')
    else:
        invest.deadline = (datetime.datetime.now() + datetime.timedelta(hours=int(tariff.end_time))).strftime(
            '%d.%m.%Y')
        invest.apply_out = int(tariff.start_time) + int(tariff.end_time) if (int(tariff.start_time) + int(tariff.end_time)) <= 24 else int(tariff.start_time) + int(tariff.end_time) - 24

    invest.procent = tariff.procent
    invest.save()

    await state.finish()
    await message.answer('Поздравляем! \nВы успешно инверстировали деньги, следить за статусом можно во вкладке '
                         'Личный кабинет', reply_markup=main_kb)
