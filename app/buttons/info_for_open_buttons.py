from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


total_kb = InlineKeyboardMarkup(row_width=1)
finish = InlineKeyboardButton('Завершить', callback_data='finish')
qr = InlineKeyboardButton('Информация для QR', callback_data='qr')
cancel = InlineKeyboardButton('Анулировать', callback_data='cancel')
total_kb.add(finish, qr, cancel)


employee_kb = InlineKeyboardMarkup()
yes = InlineKeyboardButton('Да', callback_data='yes')
no = InlineKeyboardButton('Нет', callback_data='no')
employee_kb.add(yes, no)

finish_kb = InlineKeyboardMarkup().add(finish,cancel)

