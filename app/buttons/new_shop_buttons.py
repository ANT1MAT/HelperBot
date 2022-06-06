from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


others_kb = InlineKeyboardMarkup(row_width=2)
household_goods = InlineKeyboardButton('Нужны хозяйственные товавры', callback_data='household_goods')
goods = InlineKeyboardButton('Нужен товар', callback_data='goods')
next = InlineKeyboardButton('Далее', callback_data='next')
others_kb.add(household_goods, goods, next)


check_kb = InlineKeyboardMarkup()
finish = InlineKeyboardButton('Верно', callback_data='finish')
cancel = InlineKeyboardButton('Анулировать', callback_data='cancel')
check_kb.add(finish, cancel)
