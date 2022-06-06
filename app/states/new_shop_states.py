from aiogram.dispatcher.filters.state import State, StatesGroup


class NewShop(StatesGroup):
    new_shop_data = State()
    new_shop_others = State()
    new_shop_choice = State()
    ####
    household_goods_data = State()
    household_goods_data_save = State()
    ####
    goods_data = State()
    ####
    new_shop_finish = State()



