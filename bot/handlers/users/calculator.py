from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
import datetime

from loader import dp
from sql import User, Tariff, Invest
from keyboards.default import main_kb
from utils import send_invoice, check_pay


@dp.message_handler(text='📠 Калькулятор')
@dp.message_handler(text='💲 Инвестиции')
@dp.message_handler(text='Назад', state='select_tariff')
@dp.message_handler(text='Назад', state='buy_tariff')
async def calculator(message: types.Message, state: FSMContext):
    tariffs = Tariff().select()
    tariffs_list = [el for el in tariffs]
    kb = InlineKeyboardMarkup(row_width=1)

    for el in tariffs_list:
        kb.add(InlineKeyboardButton(text=el.name, callback_data=el.id))

    await message.answer("Выберите тариф. \nПодробно с условиями всех тарифов можно ознакомиться в разделе Тарифы",
                         reply_markup=kb)
    await state.set_state('select_tariff')


@dp.callback_query_handler(state='select_tariff')
async def select_tariff(c: types.CallbackQuery, state: FSMContext):
    tariff = Tariff.get(Tariff.id == int(c.data))

    await c.message.delete()
    await c.message.answer(f"Какую сумму вы хотите рассчитать? \nНа этом тарифе можно вложить от {tariff.minimum}p до {tariff.maximum}p", reply_markup=ReplyKeyboardRemove())

    await state.set_data({'tariff': tariff})
    await state.set_state('calculate_sum')


@dp.message_handler(state='calculate_sum')
async def calculate_sum(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tariff = data['tariff']
    try:
        if int(tariff.minimum) <= int(message.text) <= int(tariff.maximum):
            data['sum'] = int(message.text)
            await state.set_data(data)
            if data['tariff'].deadline != '0':
                await message.answer("На какой срок хотите инвестировать \nУкажите число дней")
                await message.answer(f"Внимание! \nНа выбранном вами тарифе минимальный срок {data['tariff'].deadline} дней")
                await state.set_state('select_deadline')
                await state.set_data(data)
            else:
                await calculate(message, state)
        else:
            await message.answer(f"Введите сумму в диапозоне от {tariff.minimum}p до {tariff.maximum}p")
            await message.answer("Какую сумму вы хотите рассчитать?")

            await state.set_data(data)
            await state.set_state('calculate_sum')
            return
    except:
        await message.answer("Неверный формат! \nВведите только число")
        await message.answer("Какую сумму вы хотите рассчитать?")

        await state.set_data(data)
        await state.set_state('calculate_sum')


@dp.message_handler(state='select_deadline')
async def calculate(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    data = await state.get_data()
    tariff = data['tariff']
    summ = data['sum']

    if int(message.text) < int(tariff.deadline):
        await message.answer(f"Минимальный срок {tariff.deadline} дней!")
        await message.answer("На какой срок хотите инвестировать \nУкажите число дней")
        await state.set_state('select_deadline')
        await state.set_data(data)
        return
    if tariff.deadline != '0':
        percents = float(summ)*((1 + float(tariff.procent)/100)**int(message.text) - 1)
        if percents >= float(summ)*0.3:
            await message.answer(f"Слишком большой срок! \nМгновенная выплата % не может превышать 30% от тела депозита")
            await message.answer("На какой срок хотите инвестировать \nУкажите число дней")
            await state.set_state('select_deadline')
            await state.set_data(data)
            return

    text = "Ваш доход составит: \n"
    text += f'Тариф {tariff.name}\n'
    if tariff.deadline != '0':
        text += f'Вложите {float(summ)}p\n'
        text += f'Получите {str(float(summ)*((1+float(tariff.procent)/100)**float(message.text))).split(".")[0]}p\n'
        text += f'Мгновенная выплата % {str(float(summ)*((1+float(tariff.procent)/100)**float(message.text)-1)).split(".")[0]}p\n\n '
        text += f'Вернём тело депозита через {int(message.text)} дней\n'
        text += "Тело депозита возвращается по истечению срока инвестиции"
    else:
        text += f'Действует c {tariff.start_time}:00 до {f"{int(tariff.start_time) + int(tariff.end_time)}:00 часов" if (int(tariff.start_time) + int(tariff.end_time)) <= 24 else f"{int(tariff.start_time) + int(tariff.end_time) - 24}:00 часов следующего дня"}\n' if tariff.start_time != '-1' else ' '
        text += f'Сумма выплаты {str(float(summ)*(1+float(tariff.procent)/100)).split(".")[0]}\n\n'
        text += "Тело депозита возвращается вместе с % по истечению срока инвестиции"

    if tariff.deadline == '0' and \
            int(tariff.start_time)-3 <= datetime.datetime.now().hour + int(user.time_zone) < int(tariff.start_time):
        await message.answer(text, reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='Купить этот тариф', callback_data='buy_tariff')
        ))
    elif tariff.deadline != '0':
        await message.answer(text, reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='Купить этот тариф', callback_data='buy_tariff')
        ))
    else:
        text += '\n\nТариф доступен к покупке за 3 часа до начала его действия'
        await message.answer(text)

    data['deadline'] = int(message.text)
    await state.set_data(data)
    await state.set_state('buy_tariff')


@dp.callback_query_handler(state='buy_tariff')
async def select_sum(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff = data['tariff']
    summ = data['sum']
    deadline = data['deadline']
    user = User.get(User.tg_id == c.from_user.id)

    await c.message.delete()

    text = f'Ваш вклад {float(summ)}p\n'
    text += f'Доходность {float(tariff.procent)}%\n'
    text += f'Срок размещения {deadline} дней \n' if tariff.deadline != '0' else f'Срок размещения {float(tariff.end_time)} часов \n'
    if tariff.deadline != '0':
        text += f'Сумма выплаты {str(float(summ)*((1+float(tariff.procent)/100)**float(deadline))).split(".")[0]}\n\n'
        text += f'  Мгновенная выплата % {str(float(summ)*((1+float(tariff.procent)/100)**float(deadline)-1)).split(".")[0]}p\n\n '
        text += f'  Вернём тело депозита через {int(deadline)} дней\n'
        text += "Тело депозита возвращается по истечению срока инвестиции"
    else:
        text += f'Сумма выплаты {str(float(summ)*(1+float(tariff.procent)/100)).split(".")[0]}\n\n'
        text += "Тело депозита возвращается вместе с % по истечению срока инвестиции"

    if float(user.balance) < float(summ):
        text += "Сейчас на эвашем балансе недостаточно средств\n"
        text += "Пополнить баланс👇"
        await c.message.answer(text, reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="Пополнить", url=send_invoice(amount=float(summ)+5-float(user.balance),
                                                                    code=user.tg_id)),
            InlineKeyboardButton(text="Пополнил, оплатить тариф", callback_data='check_and_pay')
        ))
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
    text = tariff.get_info(buy=True, summ=float(summ))

    await c.message.answer(text=text, reply_markup=kb)
    await state.set_data(data)
    await state.set_state('buy_tariff')


@dp.message_handler(text='Оплатить', state='buy_tariff')
async def buy_tariff(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tariff = data['tariff']
    user = User.get(User.tg_id == message.from_user.id)

    user.balance = float(user.balance) - float(data['sum'])
    if tariff.deadline != '0':
        user.balance = str(float(user.balance) + float(data['sum']) * (
                    (1 + float(tariff.procent) / 100) ** int(data['deadline']) - 1)).split(".")[0]
    user.save()

    invest = Invest()
    invest.name = tariff.name
    invest.user = user.id
    if tariff.deadline == '0':
        invest.sum = str(float(user.balance) + float(data['sum']) * (1 + float(tariff.procent) / 100)).split(".")[0]
    else:
        invest.sum = f'{data["sum"]} 0'
    if tariff.start_time == '-1':
        invest.deadline = (datetime.datetime.now() + datetime.timedelta(days=float(data['deadline']))).strftime('%d.%m.%Y')
        invest.apply_out = datetime.datetime.now().strftime('%d.%m.%Y')
    else:
        invest.deadline = (datetime.datetime.now() + datetime.timedelta(hours=float(tariff.end_time))).strftime(
            '%d.%m.%Y')
        invest.apply_out = float(tariff.start_time) + float(tariff.end_time) if (float(tariff.start_time) + float(tariff.end_time)) <= 24 else float(tariff.start_time) + float(tariff.end_time) - 24

    invest.procent = tariff.procent
    invest.save()

    await state.finish()
    await message.answer('Поздравляем! \nВы успешно инверстировали деньги, следить за статусом можно во вкладке '
                         'Личный кабинет', reply_markup=main_kb)


@dp.callback_query_handler(text='check_and_pay', state='select_sum')
async def check_and_pay(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff = data['tariff']
    user = User.get(User.tg_id == c.from_user.id)

    invoice = check_pay(user.tg_id)
    if invoice:
        user.balance = float(user.balance) + float(invoice.money)
        user.save()

    if float(user.balance) < float(data['sum']):
        await c.message.answer("Для покупки тарифа необходимо пополнить баланс", reply_markup=InlineKeyboardMarkup(
            row_width=1).add(
            InlineKeyboardButton(text="Пополнить",
                                 url=send_invoice(amount=float(data['sum']) + 5 - float(user.balance),
                                                  code=user.tg_id)),
            InlineKeyboardButton(text="Пополнил, оплатить тариф", callback_data='check_and_pay')
        ))
        await state.set_data(data)
        await state.set_state('select_sum')
        return

    user.balance = float(user.balance) - float(data['sum'])
    if tariff.deadline != '0':
        user.balance = str(float(user.balance) + float(data['sum']) * (
                    (1 + float(tariff.procent) / 100) ** int(data['deadline']) - 1)).split(".")[0]

    invest = Invest()
    invest.name = tariff.name
    invest.user = user.id
    if tariff.deadline == '0':
        invest.sum = str(float(user.balance) + float(data['sum']) * (1 + float(tariff.procent) / 100)).split(".")[0]
    else:
        invest.sum = f'{data["sum"]} 0'
    if tariff.start_time == '-1':
        invest.deadline = (datetime.datetime.now() + datetime.timedelta(days=float(data['deadline']))).strftime('%d.%m.%Y')
        invest.apply_out = datetime.datetime.now().strftime('%d.%m.%Y')
    else:
        invest.deadline = (datetime.datetime.now() + datetime.timedelta(hours=float(tariff.end_time))).strftime(
            '%d.%m.%Y')
        invest.apply_out = float(tariff.start_time) + float(tariff.end_time) if (float(tariff.start_time) + float(tariff.end_time)) <= 24 else float(tariff.start_time) + float(tariff.end_time) - 24

    invest.procent = tariff.procent
    invest.save()

    await state.finish()
    await c.message.answer('Поздравляем! \nВы успешно инверстировали деньги, следить за статусом можно во вкладке '
                         'Личный кабинет', reply_markup=main_kb)
