from aiogram import types
from bot import dp, bot, cancel_kb
from aiogram.dispatcher import FSMContext
from states.task_list_states import TaskList
from buttons.task_list_buttons import task_kb, completed_task_kb, close_hg, return_hg, close_goods, return_goods, cancel
from database_query import search_task_list, search_description, change_task_query, search_completed_task_list,\
    get_user_id
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_media import InputMediaPhoto
from handler.start import start_message


@dp.callback_query_handler(lambda c: c.data == 'task_list')
async def search_task(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    tasks_technique, tasks_new_shop, tasks_info = await search_task_list(callback_query.from_user.id)
    await TaskList.search_task.set()
    start_id = 1
    answer = ''
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i, task in enumerate(tasks_technique, start=1):
        task_name = f'{i}. {task["address"]} (Т)'
        answer += task_name + '\n'
        await state.update_data({task_name: {'table_name': 'technique', 'id': task["id"]}})
        key = KeyboardButton(task_name)
        keyboard.add(key)
        start_id = i + 1
    for i, task in enumerate(tasks_new_shop, start=start_id):
        task_name = f'{i}. {task["address"]} (НМ)'
        answer += task_name + '\n'
        await state.update_data({task_name: {'table_name': 'new_shop', 'id': task["id"]}})
        key = KeyboardButton(task_name)
        keyboard.add(key)
        start_id = i + 1
    for i, task in enumerate(tasks_info, start=start_id):
        task_name = f'{i}. {task["address"]} (И)'
        answer += task_name + '\n'
        await state.update_data({task_name: {'table_name': 'info', 'id': task["id"]}})
        key = KeyboardButton(task_name)
        keyboard.add(key)
    await TaskList.next()
    if answer == '':
        answer += 'Активных задач нет'
        await state.finish()
    await bot.send_message(callback_query.from_user.id, answer, reply_markup=keyboard)
    await bot.send_message(callback_query.from_user.id, 'Отменить действие', reply_markup=cancel_kb)


@dp.callback_query_handler(lambda c: c.data == 'complеted_task')
async def search_completed_task(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    tasks_technique, tasks_new_shop, tasks_info = await search_completed_task_list(callback_query.from_user.id)
    await TaskList.search_task.set()
    start_id = 1
    answer = ''
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i, task in enumerate(tasks_technique, start=1):
        task_name = f'{i}. {task["address"]} (Т)'
        answer += task_name + '\n'
        await state.update_data({task_name: {'table_name': 'technique', 'id': task["id"]}})
        key = KeyboardButton(task_name)
        keyboard.add(key)
        start_id = i + 1
    for i, task in enumerate(tasks_new_shop, start=start_id):
        task_name = f'{i}. {task["address"]} (НМ)'
        answer += task_name + '\n'
        await state.update_data({task_name: {'table_name': 'new_shop', 'id': task["id"]}})
        key = KeyboardButton(task_name)
        keyboard.add(key)
        start_id = i + 1
    for i, task in enumerate(tasks_info, start=start_id):
        task_name = f'{i}. {task["address"]} (И)'
        answer += task_name + '\n'
        await state.update_data({task_name: {'table_name': 'info', 'id': task["id"]}})
        key = KeyboardButton(task_name)
        keyboard.add(key)
    await TaskList.next()
    if answer == '':
        answer += 'Завершенных задач нет'
        await state.finish()
    await bot.send_message(callback_query.from_user.id, answer, reply_markup=keyboard)
    await bot.send_message(callback_query.from_user.id, 'Отменить действие', reply_markup=cancel_kb)


@dp.message_handler(state=TaskList.view_task)
async def task_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get(message.text):
        table = data.get(message.text)['table_name']
        task_id = data.get(message.text)['id']
        await state.update_data(complete_task={'table_name': table, 'id': task_id})
        result, status, photo, user = await search_description(table, task_id, message.from_user.id)
        print(status)
        await state.update_data(created_task_use=user)
        await state.update_data(message=result)
        await message.answer(result)
        if photo:
            media = []
            for p in photo:
                media.append(InputMediaPhoto(p))
            await bot.send_media_group(message.from_user.id, media)
        if type(status) is dict:
            keyboard = InlineKeyboardMarkup(row_width=2)
            if status.get('status_hg') == 0:
                keyboard.add(close_hg)
            if status.get('status_hg') == 1:
                keyboard.add(return_hg)
            if status.get('status_goods') == 0:
                keyboard.add(close_goods)
            if status.get('status_goods') == 1:
                keyboard.add(return_goods)
            keyboard.add(cancel)
            return await message.answer(status, reply_markup=keyboard)
        if status == 0:
            await message.answer('Что делаем дальше?', reply_markup=task_kb)
        else:
            await message.answer('Что делаем дальше?', reply_markup=completed_task_kb)
    else:
        await message.answer('Ошибка ввода, вернитесь в меню')
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'complete', state=TaskList.view_task)
async def complete_task(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    table = data['complete_task']['table_name']
    task_id = data['complete_task']['id']
    creator_task_user_id = await get_user_id(data['created_task_use'])
    await change_task_query(table, task_id, 1, callback_query.from_user.username)
    await bot.send_message(creator_task_user_id, f'Задача ниже была закрыта.\n'
                                                 f'Задачу закрыл: @{callback_query.from_user.username}')
    await bot.send_message(creator_task_user_id, data['message'])
    await state.finish()
    await bot.send_message(callback_query.from_user.id, 'Задача закрыта')
    await start_message(message=callback_query)


@dp.callback_query_handler(lambda c: c.data == 'return_to_work', state=TaskList.view_task)
async def return_to_work_task(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    table = data['complete_task']['table_name']
    task_id = data['complete_task']['id']
    await change_task_query(table, task_id, 0, callback_query.from_user.username)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, 'Задача возвращена в работу')
    await start_message(message=callback_query)


@dp.callback_query_handler(lambda c: c.data == 'return', state=TaskList.view_task)
async def return_to_start(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    return await start_message(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'return_hg' or c.data == 'return_goods', state=TaskList.view_task)
async def return_new_shop_task(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    table = data['complete_task']['table_name']
    task_id = data['complete_task']['id']
    if callback_query.data == 'return_goods':
        status_name = 'status_goods'
    else:
        status_name = 'status_hg'
    await change_task_query(table, task_id, 0, callback_query.from_user.username, status_name)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, 'Задача возвращена в работу')
    await start_message(message=callback_query)


@dp.callback_query_handler(lambda c: c.data == 'close_hg' or c.data == 'close_goods', state=TaskList.view_task)
async def close_new_shop_task(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    table = data['complete_task']['table_name']
    task_id = data['complete_task']['id']
    if callback_query.data == 'close_goods':
        status_name = 'status_goods'
    else:
        status_name = 'status_hg'
    await change_task_query(table, task_id, 1, callback_query.from_user.username, status_name)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, 'Задача закрыта')
    await start_message(message=callback_query)

