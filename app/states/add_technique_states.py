from aiogram.dispatcher.filters.state import State, StatesGroup

class Technique(StatesGroup):
    tech_address = State()
    tech_add_product = State()
    tech_total = State()
    tech_finish = State()


