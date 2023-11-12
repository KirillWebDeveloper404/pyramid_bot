from aiogram import executor

from loader import dp, bot, scheduler
from sql import Messages
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils import add_percent, add_percent_short_tariff
from data.config import DEBUG


async def check_msg():
    msg = [el for el in Messages.select().where(Messages.address.contains("_admin_send"))]
    for el in msg:
        await bot.send_message(
            chat_id=el.address.replace("_admin_send", ''),
            text=el.text
        )
        el.address = el.address.replace("_send", '')
        el.save()


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    if not DEBUG:
        scheduler.add_job(check_msg, "interval", seconds=10)
        scheduler.add_job(add_percent, "cron", hour=10, minute=0)
        scheduler.add_job(add_percent_short_tariff, "interval", hours=1)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

