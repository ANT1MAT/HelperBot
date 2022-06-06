import importlib
from bot import dp
from aiogram import executor



importlib.import_module('handler.start')
importlib.import_module('handler.create_new_shop')
importlib.import_module('handler.info_for_open')
importlib.import_module('handler.add_technique')
importlib.import_module('handler.task_list')


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except:
            continue

