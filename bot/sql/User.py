from .BaseModel import BaseModel
from peewee import *

import datetime


class User(BaseModel):
    tg_id = TextField()
    balance = TextField(default=0)
    time_zone = TextField(default=0)
    referal = TextField(default=0)

    class Meta:
        table_name = 'panel_user'


class Tariff(BaseModel):
    name = TextField()
    procent = TextField()
    deadline = TextField()
    minimum = TextField()
    maximum = TextField()
    start_time = TextField()
    end_time = TextField()

    def get_info(self, buy=False, summ=0) -> str:
        text = f'Тариф: {self.name}\n\n'
        text += f'Доходность: {self.procent}% \n'
        if buy:
            text += f'Сумма: {summ}p\n'
        else:
            text += f'Минимальный срок: {self.deadline} дней \n' if self.start_time == -1 else ''
            text += f'Минимальная сумма: {self.minimum}p \n'
            text += f'Максимальная сумма: {self.maximum}p \n'
        text += f'Действует c {self.start_time}:00 до {f"{int(self.start_time) + int(self.end_time)}:00 часов" if (int(self.start_time) + int(self.end_time)) <= 24 else f"{int(self.start_time) + int(self.end_time) - 24} часов следующего дня"}' if self.start_time != '-1' else ''
        return text

    class Meta:
        table_name = 'panel_tariff'


class Invest(BaseModel):
    name = TextField()
    user = TextField()
    procent = TextField()
    deadline = TextField()
    apply_out = TextField()
    sum = TextField()

    def get_info(self) -> str:
        sum = self.sum.split(" ")
        text = f'Тариф {self.name}\n\n'
        text += f'Закончится: {self.deadline}\n'
        text += f'Можно снять проценты: {self.apply_out}\n\n' if "." in self.apply_out else ''
        text += f'Сумма(депозит+проценты): {int(sum[0])+int(sum[1])}p\n'
        text += f'Из них проценты: {sum[1]}p\n'
        text += f'Ставка: {self.procent}%\n'
        return text

    class Meta:
        table_name = 'panel_invest'


class History(BaseModel):
    pay_id = TextField()
    user = TextField()
    money = TextField()
    in_out = BooleanField()

    class Meta:
        table_name = 'panel_history'


class MoneyOut(BaseModel):
    money = TextField()
    card = TextField()
    user = TextField()

    class Meta:
        table_name = 'panel_moneyout'


class Messages(BaseModel):
    address = TextField()
    text = TextField()

    class Meta:
        table_name = "panel_messages"
