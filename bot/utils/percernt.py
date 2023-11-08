from sql import User, Invest
import datetime


def add_percent():
    invest = Invest.select()

    for el in invest:
        if el.deadline != el.apply_out:
            sum = el.sum.split(' ')
            el.sum = f'{str(float(sum[0])*(1+float(el.procent)/100)).split(".")[0]} {str(float(sum[0])*(1+float(el.procent)/100) - float(sum[0]) + float(sum[1])).split(".")[0]}'
            el.save()

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
            sum = el.sum.split(' ')
            el.sum = f'{str(float(sum[0])*(1+float(el.procent)/100)).split(".")[0]} {str(float(sum[0])*(1+float(el.procent)/100) - float(sum[0]) + float(sum[1])).split(".")[0]}'
            el.save()

            user = User.get(User.id == el.user)
            user.balance = int(user.balance) + int(el.sum.split(' ')[0])
            user.save()
            el.delete_instance()

