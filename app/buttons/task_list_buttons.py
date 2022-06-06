from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
task_kb = InlineKeyboardMarkup()
completed_task_kb = InlineKeyboardMarkup()

yes = InlineKeyboardButton('Завершить задачу', callback_data='complete')
return_to_work = InlineKeyboardButton('Вернуть задачу', callback_data='return_to_work')
cancel = InlineKeyboardButton('Вернуться в стартовое меню', callback_data='return')

task_kb.add(yes, cancel)
completed_task_kb.add(return_to_work, cancel)