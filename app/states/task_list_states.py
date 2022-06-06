from aiogram.dispatcher.filters.state import State, StatesGroup


class TaskList(StatesGroup):
    search_task = State()
    view_task = State()
