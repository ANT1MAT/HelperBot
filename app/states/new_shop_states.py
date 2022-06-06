from aiogram.dispatcher.filters.state import State, StatesGroup


class NewShop(StatesGroup):
    choise_stock = State()
    new_shop_data = State()
    new_shop_others = State()
    new_shop_choice = State()
    ####
    household_goods_stock = State()
    household_goods_schedule = State()
    household_goods_data = State()
    household_goods_data_save = State()
    ####
    goods_stock = State()
    goods_data = State()
    ####
    new_shop_finish = State()



