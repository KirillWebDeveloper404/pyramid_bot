from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from loader import dp
from sql import Tariff


@dp.message_handler(text='📠 Калькулятор')
async def calculator(message: types.Message, state: FSMContext):
    await message.answer("Какую сумму вы хотите рассчитать?")
    await state.set_state('calculate')


@dp.message_handler(state='calculate')
async def calculate(message: types.Message, state: FSMContext):
    tariffs = Tariff.select()
    text = "Ваш доход составит: \n"
    for el in tariffs:
        text += f'Тариф {el.name}\n'
        if el.deadline != '0':
            text += f'  Минимальный срок {el.deadline} дней\n'
            text += f'  Вложите {float(message.text)}\n'
            text += f'  Получите {str(float(message.text)*((1+float(el.procent)/100)**float(el.deadline))).split(".")[0]}\n\n'
        else:
            text += f'Действует c {el.start_time}:00 до {f"{int(el.start_time) + int(el.end_time)}:00 часов" if (int(el.start_time) + int(el.end_time)) <= 24 else f"{int(el.start_time) + int(el.end_time) - 24} часов следующего дня"}' if el.start_time != '-1' else ''
            text += f'  Вложите {float(message.text)}\n'
            text += f'  Получите {str(float(message.text)*(1+float(el.procent)/100)).split(".")[0]}\n\n'

    await message.answer(text)
