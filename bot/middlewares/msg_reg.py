from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from sql import Messages


class MsgRegMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User, chat: types.Chat = None):
        pass

    async def on_pre_process_message(self, message: types.Message, data: dict):
        msg = Messages()
        msg.address = message.from_user.id
        msg.text = message.text
        msg.save()

        await self.setup_chat(data, message.from_user, message.chat)
