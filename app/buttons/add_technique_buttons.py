from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

tech_kb = InlineKeyboardMarkup()

finish = InlineKeyboardButton('Завершить', callback_data='finish')
add = InlineKeyboardButton('Добавить ещё товар', callback_data='add')
cancel = InlineKeyboardButton('Анулировать', callback_data='cancel')

tech_kb.add(finish, add, cancel)

