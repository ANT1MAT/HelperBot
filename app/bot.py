import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middleware.cheak_user import CheckUser
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


with open('config.json', 'r') as file:
    config = json.load(file)
    API_TOKEN = config['token']


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

cancel_button = InlineKeyboardButton('Отмена', callback_data='cancel')
cancel_kb = InlineKeyboardMarkup().add(cancel_button)


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Все действия отменены.\n'
                         'Для возврата в меню нажмите /start', reply_markup=ReplyKeyboardRemove())


dp.middleware.setup(CheckUser())
dp.register_message_handler(cancel, text=['Отмена'], state='*')
dp.register_message_handler(cancel, commands='cancel', state='*')
