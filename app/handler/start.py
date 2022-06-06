from aiogram import types
from bot import dp, bot
from buttons.menu_buttons import menu_kb_user, menu_kb_ref_stock, menu_kb_admin
from database_query import check_user, add_user, user_status_check


@dp.message_handler(commands='start', state='*')
async def start_message(message: types.Message):
    if await check_user(message.from_user.id) and await user_status_check(message.from_user.id):
        user_status = await user_status_check(message.from_user.id)
        if user_status == 1:
            await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}.\n'
                                                         f'Команды, которые понимает бот:\n'
                                                         f'/start - начальное меню,\n'
                                                         f'/cancel - отмена всех действий.',
                                          reply_markup=menu_kb_user)
        if user_status == 2 or user_status == 3:
            await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}.\n'
                                                         f'Команды, которые понимает бот:\n'
                                                         f'/start - начальное меню,\n'
                                                         f'/cancel - отмена всех действий.',
                                          reply_markup=menu_kb_ref_stock)
        if user_status == 4:
            await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}.\n'
                                                         f'Команды, которые понимает бот:\n'
                                                         f'/start - начальное меню,\n'
                                                         f'/cancel - отмена всех действий.',
                                          reply_markup=menu_kb_admin)
    else:
        await add_user(message.from_user.id, message.from_user.username)
        await message.answer(f'Ваши данные отправлены для добавления, ожидайте')


