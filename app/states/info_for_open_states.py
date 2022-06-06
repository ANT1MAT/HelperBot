from aiogram.dispatcher.filters.state import State, StatesGroup


class InfoStates(StatesGroup):
    info_address = State()
    info_date = State()
    info_coordinates = State()
    info_schedule = State()
    info_description = State()
    info_total = State()
    info_area = State()
    info_area_save = State()
    info_passport = State()
    info_snils = State()
    info_add_employee = State()
    info_photo_markup = State()
    info_photo_screen = State()
    info_photo_household_goods = State()
    info_finish = State()

