from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu_kb_user = InlineKeyboardMarkup(row_width=1)
menu_kb_ref_stock = InlineKeyboardMarkup(row_width=1)
menu_kb_admin = InlineKeyboardMarkup(row_width=1)
create_new_shop = InlineKeyboardButton('Открытие нового магазина', callback_data='new_shop')
info_for_open = InlineKeyboardButton('Информация для открытия', callback_data='info_for_open')
technique = InlineKeyboardButton('Техника', callback_data='technique')
task_list = InlineKeyboardButton('Просмотр задач', callback_data='task_list')
completed_task_list = InlineKeyboardButton('Просмотр завершенных задач', callback_data='complеted_task')


menu_kb_user.add(create_new_shop, info_for_open, technique)
menu_kb_ref_stock.add(task_list, completed_task_list)
menu_kb_admin.add(create_new_shop, info_for_open, technique, task_list, completed_task_list)

stock_kb = InlineKeyboardMarkup(row_width=2)
cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
stock_msk = InlineKeyboardButton('Склад МСК', callback_data='stock_msk')
stock_spb = InlineKeyboardButton('Склад СПб', callback_data='stock_spb')
stock_kb.add(stock_spb, stock_msk, cancel)

