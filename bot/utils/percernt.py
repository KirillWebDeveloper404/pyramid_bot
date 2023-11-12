from sql import User, Invest
import datetime


def add_percent():
    invest = Invest.select()

    for el in invest:
        if el.deadline != el.apply_out:
            if datetime.datetime.now() >= datetime.datetime.strptime(el.deadline, '%d.%m.%Y'):
                user = User.get(User.id == el.user)
                user.balance = int(user.balance) + int(el.sum.split(' ')[0])
                user.save()
                el.delete_instance()


def add_percent_short_tariff():
    invest = Invest.select()

    for el in invest:
        now = datetime.datetime.now().hour
        if "." not in el.apply_out \
                and datetime.datetime.now() >= datetime.datetime.strptime(el.deadline, '%d.%m.%Y') \
                and now >= int(el.apply_out):
            user = User.get(User.id == el.user)
            user.balance = int(user.balance) + int(el.sum.split(' ')[0])
            user.save()
            el.delete_instance()

