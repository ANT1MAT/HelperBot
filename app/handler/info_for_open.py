from aiogram import types
from bot import dp, bot, cancel_kb
from aiogram.dispatcher import FSMContext
from states.info_for_open_states import InfoStates
from buttons.info_for_open_buttons import total_kb, employee_kb, finish_kb
from aiogram.types.input_media import InputMediaPhoto
from database_query import save_info, select_users
from handler.start import start_message


USER_STATUS = 4
BEST_RESOLUTION = 3


@dp.callback_query_handler(lambda c: c.data == 'info_for_open')
async def set_address(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите адрес нового магазина')
    await InfoStates.info_address.set()


@dp.message_handler(state=InfoStates.info_address)
async def set_date(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите планируемую дату открытия', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_date)
async def set_coordinates(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Введите координаты магазина', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_coordinates)
async def set_schedule(message: types.Message, state: FSMContext):
    await state.update_data(coordinates=message.text)
    await message.answer('Отправьте график работы магазина', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_schedule)
async def set_description(message: types.Message, state: FSMContext):
    await state.update_data(schedule=message.text)
    await message.answer('Отправьте описание магазина', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_total)
async def show_total(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer = (f'{data["address"]} будет открыт '
              f'{data["date"]}.\n'
              f'Координаты магазина: {data["coordinates"]}\n'
              f'График работы: {data["schedule"]}\n'
              f'Описание: {data["description"]}\n')
    await state.update_data(answer=answer)
    await message.answer(answer, reply_markup=total_kb)


@dp.message_handler(state=InfoStates.info_description)
async def save_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await InfoStates.next()
    return await show_total(message=message, state=state)


@dp.callback_query_handler(lambda c: c.data == 'qr', state=InfoStates.info_total)
async def set_entity(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Какое Юр. лицо будет по данному адресу', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_area)
async def set_area(message: types.Message, state: FSMContext):
    await state.update_data(entity=message.text)
    await message.answer('Сколько квадратных метров площадь зала?', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_area_save)
async def save_area(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text)
    await InfoStates.next()
    return await set_passport(user_id=message.from_user.id, state=state)


@dp.message_handler(state=InfoStates.info_passport)
async def set_passport(user_id: None, state: FSMContext):
    await bot.send_message(user_id, 'Отправьте серию и номер паспорта сотрудника(без пробелов и тире)',
                           reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_snils)
async def set_snils(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('passport_1'):
        await state.update_data(passport_2=message.text)
    else:
        await state.update_data(passport_1=message.text)
    await message.answer('Отправьте СНИЛС сотрудника (11 цифр без пробелов и тире)', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(state=InfoStates.info_add_employee)
async def add_second_employee(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('snils_1'):
        await state.update_data(snils_2=message.text)
        await InfoStates.info_photo_markup.set()
        return await set_markup(user_id=message.from_user.id)
    else:
        await state.update_data(snils_1=message.text)
        await message.answer('Отправить данные ещё одного сотрудника', reply_markup=employee_kb)


@dp.callback_query_handler(lambda c: c.data == 'yes', state=InfoStates.info_add_employee)
async def add_second_employee(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await InfoStates.info_passport.set()
    return await set_passport(user_id=callback_query.from_user.id, state=state)


@dp.callback_query_handler(lambda c: c.data == 'no', state=InfoStates.info_add_employee)
async def switch_state(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await InfoStates.next()
    return await set_markup(user_id=callback_query.from_user.id)


async def set_markup(user_id: None):
    await bot.send_message(user_id, 'Отпарвьте фото разметки на полу (как минимум 2 полосы в кадре',
                           reply_markup=cancel_kb)


@dp.message_handler(content_types=['photo'], state=InfoStates.info_photo_markup)
async def set_screen(message: types.Message, state: FSMContext):
    await state.update_data(photo_markup=message.photo[BEST_RESOLUTION]['file_id'])
    await message.answer('Отправьте фото защитного экрана (его должно быть видно полность)', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(content_types=['photo'], state=InfoStates.info_photo_screen)
async def set_household(message: types.Message, state: FSMContext):
    await state.update_data(photo_screen=message.photo[BEST_RESOLUTION]['file_id'])
    await message.answer('Отправьте фото с масками и антисептиками', reply_markup=cancel_kb)
    await InfoStates.next()


@dp.message_handler(content_types=['photo'], state=InfoStates.info_photo_household_goods)
async def save_household(message: types.Message, state: FSMContext):
    await state.update_data(photo_household=message.photo[BEST_RESOLUTION]['file_id'])
    await InfoStates.next()
    return await info_finish(user_id=message.from_user.id, state=state)


@dp.message_handler(state=InfoStates.info_finish)
async def info_finish(user_id: None, state: FSMContext):
    data = await state.get_data()
    answer = (f'{data["address"]} будет открыт '
              f'{data["date"]}.\n'
              f'Координаты магазина: {data["coordinates"]}\n'
              f'График работы: {data["schedule"]}\n'
              f'Описание: {data["description"]}\n\n'
              f'Данные для QR кода:\n'
              f'Юр.лицо:{data["entity"]}\n'
              f'Площадь торгового зала:{data["area"]}\n')
    await state.update_data(answer=answer)
    if data.get('passport_2') and data.get('snils_2'):
        answer += 'Поданы данные о 2 сотрудниках\n'
    else:
        answer += 'Поданы данные о 1 сотруднике\n'
    if data.get('photo_markup') and data.get('photo_screen') and\
            data.get('photo_household'):
        answer += 'Все фотографии загружены'
    else:
        answer +='Загружены не все фото'

    media = [InputMediaPhoto(data['photo_markup']), InputMediaPhoto(data['photo_screen']),
             InputMediaPhoto(data['photo_household'])]
    await bot.send_media_group(user_id, media)
    await bot.send_message(user_id, answer, reply_markup=finish_kb)


@dp.callback_query_handler(lambda c: c.data == 'finish', state=[InfoStates.info_finish, InfoStates.info_total])
async def save_data(callback_query: types.callback_query, state: FSMContext):
    await state.update_data(status=[USER_STATUS])
    await state.update_data(created_task_user=callback_query.from_user.username)
    data = await state.get_data()
    answer = data['answer']
    if data.get('passport_1') and data.get('snils_1'):
        answer += (f'1 сотрудник:\n'
                  f'Паспорт:{data["passport_1"]}\n'
                  f'СНИЛС:{data["snils_1"]}\n')
    if data.get('passport_2') and data.get('snils_2'):
        answer += (f'1 сотрудник:\n'
                  f'Паспорт:{data["passport_2"]}\n'
                  f'СНИЛС:{data["snils_2"]}\n')
    if data.get('photo_markup') and data.get('photo_screen') and data.get('photo_household'):
        answer += 'Все фотографии загружены'
    else:
        answer +='Загруженны не все фото'
    await bot.answer_callback_query(callback_query.id)
    await save_info(data)
    await bot.send_message(callback_query.from_user.id, 'Заявка принята')
    users = await select_users(data['status'])
    for user in users:
        await bot.send_message(user, answer)
    await state.finish()
    await start_message(message=callback_query)



