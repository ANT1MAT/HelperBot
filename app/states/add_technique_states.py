from aiogram.dispatcher.filters.state import State, StatesGroup


class Technique(StatesGroup):
    choise_stock = State()
    tech_address = State()
    tech_add_product = State()
    tech_total = State()
    tech_finish = State()


