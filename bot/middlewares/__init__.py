from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .msg_reg import MsgRegMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(MsgRegMiddleware())
