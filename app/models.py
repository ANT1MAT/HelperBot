from sqlalchemy import Table, Column, Integer, String, MetaData


meta = MetaData()

#1 = ТМ
#2 = склад все
#3 = хозка вся
#4 = админ
#5 = склад спб
#6 = склад мск
#7 = хозка спб
#8 = хозка мск


technique = Table(
    'technique', meta,
    Column('id', Integer, primary_key=True),
    Column('address', String),
    Column('product', String),
    Column('status', Integer),
    Column('accesses_user', String),
    Column('stock', String),
    Column('created_task_user', String),
    Column('closed_task_user', String)
)


users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('user_name', String),
    Column('accesses_user', Integer)
)

info_open = Table(
    'info_open', meta,
    Column('id', Integer, primary_key=True),
    Column('address', String),
    Column('date', String),
    Column('coordinates', String),
    Column('schedule', String),
    Column('description', String),
    Column('entity', String),
    Column('area', String),
    Column('passport_1', String),
    Column('snils_1', String),
    Column('passport_2', String),
    Column('snils_2', String),
    Column('photo_markup', String),
    Column('photo_screen', String),
    Column('photo_household', String),
    Column('status', Integer),
    Column('accesses_user', String),
    Column('created_task_user', String),
    Column('closed_task_user', String)
)


new_shop = Table(
    'new_shop', meta,
    Column('id', Integer, primary_key=True),
    Column('address', String),
    Column('open_date', String),
    Column('hg_entity', String),
    Column('hg_date', String),
    Column('hg_schedule', String),
    Column('status_hg', Integer),
    Column('goods_date', String),
    Column('status_goods', Integer),
    Column('accesses_user', String),
    Column('stock_hg', String),
    Column('stock_goods', String),
    Column('created_task_user', String),
    Column('closed_task_hg_user', String),
    Column('closed_task_goods_user', String),
)

