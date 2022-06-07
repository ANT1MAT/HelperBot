from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
task_kb = InlineKeyboardMarkup()
completed_task_kb = InlineKeyboardMarkup()

yes = InlineKeyboardButton('Завершить задачу', callback_data='complete')
return_to_work = InlineKeyboardButton('Вернуть задачу', callback_data='return_to_work')
cancel = InlineKeyboardButton('Вернуться в стартовое меню', callback_data='return')

task_kb.add(yes, cancel)
completed_task_kb.add(return_to_work, cancel)

close_hg = InlineKeyboardButton('Завершить задачу по хозяйственным товарам', callback_data='close_hg')
close_goods = InlineKeyboardButton('Завершить задачу по товарам', callback_data='close_goods')
return_hg = InlineKeyboardButton('Вернуть задачу хозяйственным товарам', callback_data='return_hg')
return_goods = InlineKeyboardButton('Вернуть задачу хозяйственным товарам', callback_data='return_goods')