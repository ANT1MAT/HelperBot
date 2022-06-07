from aiogram import types
from bot import dp, bot, cancel_kb
from aiogram.dispatcher import FSMContext
from states.add_technique_states import Technique
from buttons.add_technique_buttons import tech_kb
from database_query import save_technique, select_users
from handler.start import start_message
from buttons.menu_buttons import stock_kb


@dp.callback_query_handler(lambda c: c.data == 'technique')
async def set_stock(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете склад отправитель:', reply_markup=stock_kb)
    await Technique.choise_stock.set()


@dp.callback_query_handler(lambda c: c.data == 'stock_spb' or c.data == 'stock_msk',
                           state=Technique.choise_stock)
async def set_address(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.answer_callback_query(callback_query.id)
    await state.update_data(stock=callback_query.data)
    await bot.send_message(callback_query.from_user.id, 'Напишите адрес магазина', reply_markup=cancel_kb)
    await Technique.next()


@dp.message_handler(state=Technique.tech_address)
async def save_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await Technique.next()
    return await add_product(user_id=message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == 'add', state=Technique.tech_total)
async def add_more_product(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)
    await Technique.tech_add_product.set()
    return await add_product(user_id=callback_query.from_user.id)


async def add_product(user_id: None):
    await bot.send_message(user_id, 'Что записать на данный магазин?', reply_markup=cancel_kb)


@dp.message_handler(state=Technique.tech_add_product)
async def save_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('product'):
        data['product'].append(message.text)
        await state.update_data(product=data['product'])
    else:
        prod = list()
        prod.append(message.text)
        await state.update_data(product=prod)
    await Technique.next()
    return await tech_total(message=message, state=state)


async def tech_total(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer = f'Записать товар ниже в магазин {data["address"]}:\n'
    for i, prod in enumerate(data['product'], start=1):
        answer += f'{i}. {prod}\n'
    if data.get('stock') == 'stock_msk':
        answer += 'Склад отправитель МСК'
    else:
        answer += 'Склад отправитель СПб'
    await state.update_data(answer=answer)
    await state.update_data(created_task_user=message.from_user.username)
    await message.answer(answer, reply_markup=tech_kb)


@dp.callback_query_handler(lambda c: c.data == 'finish', state=Technique.tech_total)
async def save_data(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    await save_technique(data)
    await bot.send_message(callback_query.from_user.id, 'Товар записан')
    if data.get('stock') == 'stock_msk':
        users_status = [2, 4, 6]
    else:
        users_status = [2, 4, 5]
    users = await select_users(users_status)
    for user in users:
        await bot.send_message(user, data['answer'])
    await state.finish()
    await start_message(message=callback_query)
