from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.storage import FSMContext

from loader import dp, bot
from sql import User, History, MoneyOut
from data.config import ADMINS
from keyboards.default import main_kb
from utils import send_invoice, check_pay


@dp.callback_query_handler(text='money_out')
async def money_out(c: types.CallbackQuery, state: FSMContext):
    user = User.get(User.tg_id == c.from_user.id)
    if float(user.balance) >= 100:
        await c.message.answer(f"Ваш баланс {user.balance}p\n"
                               "Напишите номер карты либо кошелька куда хотите вывести деньги")
        await state.set_state('sum_out')
    else:
        await c.answer("Минимальная сумма вывода 100р")


@dp.message_handler(state='sum_out')
async def sum_out(message: types.Message, state: FSMContext):
    try:

        moneyout = MoneyOut()
        moneyout.user = message.from_user.id
        moneyout.card = message.text
        moneyout.money = user.balance
        moneyout.save()

        user = User.get(User.tg_id == message.from_user.id)
        user.balance = 0
        user.save()

        await message.answer(f"Заявка на вывод создана, скоро мы переведём ва деньги.")

        await bot.send_message(
            chat_id=ADMINS[0],
            text=f'Платёж \nСумма: {float(user.balance)} \nКомментарий: {user.tg_id}',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='Зачислить', callback_data=f'accept_{user.tg_id}_{message.text}'),
                InlineKeyboardButton(text='Отклонить', callback_data=f'cancel_{user.tg_id}_{message.text}'),
            )
        )

    except Exception as e:
        prfloat(e)
        await message.answer("Неверный формат! Ведите только число.")
        await state.set_state('sum_balance')


@dp.callback_query_handler(text='add_balance')
async def add_balance(c: types.CallbackQuery, state: FSMContext):
    user = User.get(User.tg_id == c.from_user.id)
    await c.message.answer(f"Ваш баланс {user.balance}p\nНа какую сумму хотите пополнить?")
    await state.set_state('sum_balance')


@dp.message_handler(state='sum_balance')
async def sum_balance(message: types.Message, state: FSMContext):
    try:
        user = User.get(User.tg_id == message.from_user.id)
        sum = float(message.text)
        invoice_link = send_invoice(amount=sum, code=str(user.tg_id))

        await message.answer(f"💰 Пополнить баланс \n\nСумма: {sum}₽", reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='Перейти к оплате', url=invoice_link),
            InlineKeyboardButton(text='Проверить оплату', callback_data='check_pay')
        ))

        await state.set_state('check_pay')
    except:
        await message.answer("Неверный формат! Ведите только число.")
        await state.set_state('sum_balance')


@dp.callback_query_handler(text='check_pay', state='*')
async def check_pay_handler(c: types.CallbackQuery, state: FSMContext):
    user = User.get(User.tg_id == c.from_user.id)
    invoice = check_pay(str(user.tg_id))
    if invoice:
        await c.message.delete()
        await state.finish()
        user.balance = float(user.balance) + float(invoice.money)
        user.save()
        await c.message.answer("Ваш баланс успешно пополнен! \nПроверить баланс можно в разделе Личный кабинет")
    else:
        await c.message.answer('Мы не нашли ваш платеж. \nВозможно он еще в обработке, попробуйте нажать "Проверить" '
                               'ещё раз.\n'
                               'Если не помогает обратитесь к администратору')


# Обязательно последним в списке!!!
# @dp.callback_query_handler()
# async def check_pay(c: types.CallbackQuery):
#     if c.message.chat.id == ADMINS[0]:
#         if 'accept' in c.data:
#             user = User.get(User.tg_id == c.data.split('_')[1])
#             user.balance = float(user.balance) + float(c.data.split('_')[2])
#             user.save()
#
#         if user.referal != '0':
#             ref = User.get(User.tg_id == user.referal)
#             ref.balance = str(float(ref.balance) + float(c.data.split('_')[2])*(1+2.5/100)).split('.')[0]
#             ref.save()
#             if ref.referal != '0':
#                 ref1 = User.get(User.tg_id == ref.referal)
#                 ref1.balance = str(float(ref1.balance) + float(c.data.split('_')[2])*(1+1/100)).split('.')[0]
#                 ref1.save()
#
#             history = History()
#             history.user = user.tg_id
#             history.money = c.data.split('_')[2]
#             history.in_out = True
#             history.save()
#
#             await bot.send_message(
#                 chat_id=c.data.split('_')[1],
#                 text=f'Платёж на сумму {c.data.split("_")[2]} подтверждён, деньги зачислены  на баланс.'
#             )
#
#             await c.message.delete()
#
#         else:
#             await bot.send_message(
#                 chat_id=c.data.split('_')[1],
#                 text=f'Платёж на сумму {c.data.split("_")[2]} отклонён, если считаете что это ошибка обратитесь в поддержку.'
#             )
#             await c.message.delete()
# # Обязательно последним в списке!!!
