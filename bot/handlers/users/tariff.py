from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
import datetime

from loader import dp
from sql import User, Tariff, Invest
from keyboards.default import main_kb


@dp.message_handler(text='🧾 Тарифы')
async def tariffs_desc(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    time_now = datetime.datetime.now().hour + int(user.time_zone)
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
        text += '4. Premium новинка "Lite money" \n'
        text += 'Пока ты спишь \n'
        text += '3% за ночь с 24:00 до 06:00 6 часов \n'
        text += 'Минимальный порог 50 000 руб \n'
        text += 'Максимальный порог 500 000 руб \n'
        text += 'Возврат тела депозита 7:00 \n'
        text += 'P.S. Тело депозита выплачивается вместе с %'

    await message.answer(text)


@dp.message_handler(text='💲 Инвестиции')
@dp.message_handler(text='Назад', state='select_tariff')
@dp.message_handler(text='Назад', state='buy_tariff')
async def list_tariff(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    time_now = datetime.datetime.now().hour + int(user.time_zone)
    tariffs = Tariff().select()
    tariffs_list = [el for el in tariffs]
    kb = InlineKeyboardMarkup(row_width=1)

    for el in tariffs_list:
        if el.start_time == '-1':
            kb.add(InlineKeyboardButton(text=el.name, callback_data=el.id))
        else:
            start_time = int(el.start_time) - 2 if int(el.start_time) - 2 >= 0 else int(el.start_time) - 2 + 24
            if start_time <= time_now < start_time+2:
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
