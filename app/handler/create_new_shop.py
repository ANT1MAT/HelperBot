from aiogram import types
from bot import dp, bot, cancel_kb
from states.new_shop_states import NewShop
from buttons.new_shop_buttons import others_kb, check_kb
from aiogram.dispatcher import FSMContext
from database_query import save_new_shop, select_users
from handler.start import start_message
from aiogram.types import ReplyKeyboardRemove


@dp.callback_query_handler(lambda c: c.data == 'new_shop')
async def set_address(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите адрес нового магазина', reply_markup=cancel_kb)
    await NewShop.new_shop_data.set()


@dp.message_handler(state=NewShop.new_shop_data)
async def set_open_date(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f'Магазин:{data["address"]}')
    await message.answer('Введите планируемую дату открытия', reply_markup=cancel_kb)
    await NewShop.next()


@dp.message_handler(state=NewShop.new_shop_others)
async def set_others(message: types.Message, state: FSMContext):
    await state.update_data(open_date=message.text)
    data = await state.get_data()
    await NewShop.next()
    await message.answer(f'Магазин: {data["address"]}\n'
                         f'Планируемая дата открытия: {data["open_date"]}', reply_markup=others_kb)


@dp.callback_query_handler(lambda c: c.data == 'household_goods', state=NewShop.new_shop_choice)
async def add_household_goods(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Какое юридическое лицо будет по данному адресу?', reply_markup=cancel_kb)
    await NewShop.next()


@dp.message_handler(state=NewShop.household_goods_data)
async def add_hg_data(message: types.Message, state: FSMContext):
    await state.update_data(hg_entity=message.text)
    await message.answer('К какому числу подготовить хозяйственные товары?', reply_markup=cancel_kb)
    await NewShop.household_goods_data_save.set()


@dp.message_handler(state=NewShop.household_goods_data_save)
async def save_hg_date(message: types.Message, state: FSMContext):
    await state.update_data(hg_date=message.text)
    return await show_total(message=message, state=state)


async def show_total(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer = (f'Магазин: {data["address"]}\n'
              f'Планируемая дата открытия: {data["open_date"]}\n')
    if data.get('hg_entity') and data.get('hg_date'):
        answer += (f'Требуются хозяйственные товары для {data["hg_entity"]}'
                   f' к {data["hg_date"]}\n')
    if data.get('goods_date'):
        answer += f'Требуется товар к {data["goods_date"]}'
    await message.answer(answer, reply_markup=others_kb)
    await NewShop.new_shop_choice.set()


@dp.callback_query_handler(lambda c: c.data == 'goods', state=NewShop.new_shop_choice)
async def add_goods_date(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Какому числу нужен товар?', reply_markup=cancel_kb)
    await NewShop.goods_data.set()


@dp.message_handler(state=NewShop.goods_data)
async def save_goods_date(message: types.Message, state: FSMContext):
    await state.update_data(goods_date=message.text)
    return await show_total(message=message, state=state)


@dp.callback_query_handler(lambda c: c.data == 'next', state=NewShop.new_shop_choice)
async def check_correctness(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Проверьте правильность данных')
    data = await state.get_data()
    status = set()
    status.add(2)
    status.add(4)
    answer = (f'Магазин: {data["address"]}\n'
              f'Планируемая дата открытия: {data["open_date"]}\n')
    if data.get('hg_entity') and data.get('hg_date'):
        answer += (f'Требуются хозяйственные товары для {data["hg_entity"]}'
                   f' к {data["hg_date"]}\n')
    if data.get('goods_date'):
        answer += f'Требуется товар к {data["goods_date"]}'
        status.add(3)
    await state.update_data(answer=answer)
    await state.update_data(status=status)
    await bot.send_message(callback_query.from_user.id, answer, reply_markup=check_kb)
    await NewShop.new_shop_finish.set()


@dp.callback_query_handler(lambda c: c.data == 'cancel', state='*')
async def save_data(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, 'Действие отменено', reply_markup=ReplyKeyboardRemove())
    await start_message(message=callback_query)


@dp.callback_query_handler(lambda c: c.data == 'finish', state=NewShop.new_shop_finish)
async def save_data(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    await save_new_shop(data)
    await bot.send_message(callback_query.from_user.id, 'Заявка принята')
    status = data.get('status')
    users = await select_users(status)
    for user in users:
        await bot.send_message(user, data['answer'])
    await state.finish()
    await start_message(message=callback_query)

