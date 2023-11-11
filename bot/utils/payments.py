from yoomoney import Client, Quickpay

from data.config import PAY_TOKEN
from sql import History


def send_invoice(amount: int, code: str) -> str:
    quickpay = Quickpay(
                receiver="4100118436096814",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=amount,
                label=code
                )

    return quickpay.redirected_url


def check_pay(code: str):
    client = Client(PAY_TOKEN)
    history = client.operation_history(label=code)
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
            return invoice

    return False
