from yoomoney import Client, Quickpay

from data.config import PAY_TOKEN
from sql import History


code = '5613860031'
client = Client(PAY_TOKEN)
history = client.operation_history(label=code)
# history = client.operation_history()
try:
    operation_list = History.select().where(History.user == code)
except History.DoesNotExist:
    operation_list = []

operation_ids = [el.pay_id for el in operation_list]

for operation in history.operations:
    if operation.status == 'success' and operation.operation_id not in operation_ids:
        invoice = History()
        invoice.user = code
        invoice.in_out = True
        invoice.pay_id = operation.operation_id
        invoice.money = operation.amount
        invoice.save()
        print(operation.label)
        print(operation.amount)
        print(operation.status)
        print(operation.datetime)
        print()
