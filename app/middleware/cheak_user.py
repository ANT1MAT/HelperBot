from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from database_query import user_status_check


class CheckUser(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user_id = update.message.from_user.id
            if update.message.text == '/start':
                return
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            raise CancelHandler()

        if await user_status_check(user_id):
            return
        else:
            raise CancelHandler()

