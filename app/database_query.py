from sqlalchemy import create_engine, exists, select, text,or_
from models import users, technique, new_shop, info_open, meta
from sqlalchemy.orm import sessionmaker
from encryption import create_hash, decode_hash

engine = create_engine('postgresql://habrpguser:pgpwd4habr@pg_db/habrdb')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
meta.create_all(engine)


async def check_user(user_id):
    return session.query(exists().where(users.c.user_id == user_id)).scalar()


async def user_status_check(user_id):
    try:
        return session.query(users.c.accesses_user).where(users.c.user_id == user_id).all()[0]['accesses_user']
    except IndexError:
        return False


async def get_user_id(username):
    return session.query(users.c.user_id).where(users.c.user_name == username).all()[0]['user_id']


async def add_user(user_id, user_name):
    if await check_user(user_id) is False:
        ins = users.insert().values(
        user_id=user_id,
        user_name=user_name,
        )
        conn.execute(ins)


async def save_technique(data: dict):
    ins = technique.insert().values(
        address=data.get('address'),
        product=repr(data.get('product')),
        status=0,
        accesses_user=4,
        stock=data.get('stock'),
        created_task_user=data.get('created_task_user')
    )
    conn.execute(ins)


async def save_new_shop(data: dict):
    ins = new_shop.insert().values(
        address=data.get('address'),
        open_date=data.get('open_date'),
        hg_entity=data.get('hg_entity'),
        hg_date=data.get('hg_date'),
        status_hg=0,
        goods_date=data.get('goods_date'),
        status_goods=0,
        accesses_user=repr(data.get('status'))[1:-1],
        stock_hg=data.get('stock_hg'),
        stock_goods=data.get('stock_goods'),
        hg_schedule=data.get('hg_schedule'),
        created_task_user=data.get('created_task_user')
    )
    conn.execute(ins)


async def save_info(data: dict):
    ins = info_open.insert().values(
        address=data.get('address'),
        date=data.get('date'),
        coordinates=data.get('coordinates'),
        schedule=data.get('schedule'),
        description=data.get('description'),
        entity=data.get('entity'),
        area=data.get('area'),
        passport_1=create_hash(data.get('passport_1')),
        snils_1=create_hash(data.get('snils_1')),
        passport_2=create_hash(data.get('passport_2')),
        snils_2=create_hash(data.get('snils_2')),
        photo_markup=data.get('photo_markup'),
        photo_screen=data.get('photo_screen'),
        photo_household=data.get('photo_household'),
        status=0,
        accesses_user=repr(data.get('status'))[1:-1],
        created_task_user=data.get('created_task_user')

    )
    conn.execute(ins)


async def select_users(status):
    result = []
    for x in session.query(users.c.user_id).where(users.c.accesses_user.in_(status)).all():
        result.append(x['user_id'])
    return result


async def search_task_list(user_id):
    user_status = await user_status_check(user_id)
    if user_status == 4:
        result_new_shop = session.query(new_shop.c.address, new_shop.c.id)\
            .where(or_(new_shop.c.status_goods == 0, new_shop.c.status_hg == 0))\
            .filter(new_shop.c.accesses_user.ilike(f'%{user_status}%')).all()
    elif user_status in [2, 5, 6]:
        result_new_shop = session.query(new_shop.c.address, new_shop.c.id).where(new_shop.c.status_goods == 0)\
                                             .filter(new_shop.c.accesses_user.ilike(f'%{user_status}%')).all()
    elif user_status in [3, 7, 8]:
        result_new_shop = session.query(new_shop.c.address, new_shop.c.id).where(new_shop.c.status_hg == 0)\
                                          .filter(new_shop.c.accesses_user.ilike(f'%{user_status}%')).all()
    result_info = session.query(info_open.c.address, info_open.c.id)\
        .where(info_open.c.status == 0)\
        .filter(info_open.c.accesses_user.ilike(f'%{user_status}%')).all()
    result_technique = session.query(technique.c.address, technique.c.id)\
        .where(technique.c.status == 0)\
        .filter(technique.c.accesses_user.ilike(f'%{user_status}%')).all()
    return result_technique, result_new_shop, result_info


async def search_completed_task_list(user_id):
    user_status = await user_status_check(user_id)
    if user_status == 4:
        result_new_shop = session.query(new_shop.c.address, new_shop.c.id)\
            .where(or_(new_shop.c.status_goods == 1, new_shop.c.status_hg == 1))\
            .filter(new_shop.c.accesses_user.ilike(f'%{user_status}%')).all()
    elif user_status in [2, 5, 6]:
        result_new_shop = session.query(new_shop.c.address, new_shop.c.id).where(new_shop.c.status_goods == 1)\
                                             .filter(new_shop.c.accesses_user.ilike(f'%{user_status}%')).all()
    elif user_status in [3, 7, 8]:
        result_new_shop = session.query(new_shop.c.address, new_shop.c.id).where(new_shop.c.status_hg == 1)\
                                          .filter(new_shop.c.accesses_user.ilike(f'%{user_status}%')).all()
    result_info = session.query(info_open.c.address, info_open.c.id)\
        .where(info_open.c.status == 1)\
        .filter(info_open.c.accesses_user.ilike(f'%{user_status}%')).all()
    result_technique = session.query(technique.c.address, technique.c.id)\
        .where(technique.c.status == 1)\
        .filter(technique.c.accesses_user.ilike(f'%{user_status}%')).all()
    return result_technique, result_new_shop, result_info


async def search_description(table, task_id, user_id):
    if table == 'technique':
        result = session.query(technique).where(technique.c.id == task_id).all()[0]
        answer = ''
        if result['stock'] == 'stock_msk':
            answer += '[МСК]'
        else:
            answer += '[СПб]'
        answer += f'В магазин {result["address"]} требуется:\n'
        products = eval(result["product"])
        for i, prod in enumerate(products, start=1):
            answer += f'{i}. {prod}\n'
        answer += f'Задачу создал @{result["created_task_user"]}\n'
        return answer, result['status'], None, result['created_task_user']
    elif table == 'new_shop':
        status = dict()
        user_status = await user_status_check(user_id)
        answer = ''
        result = session.query(new_shop).where(new_shop.c.id == task_id).all()[0]
        if result['stock_hg'] and result['status_hg'] == 0:
            if result['stock_hg'] == 'stock_msk':
                answer += '[Хозка с МСК]'
            else:
                answer += '[Хозка с СПб]'
        if result['stock_goods'] and result['status_goods'] == 0:
            if result['stock_goods'] == 'stock_msk':
                answer += '[Товары с МСК]'
            else:
                answer += '[Товары с СПб]'
        answer += (f'Магазин: {result["address"]}\n'
                  f'Планируемая дата открытия: {result["open_date"]}\n')
        if result["hg_entity"] and result["hg_date"] and result['status_hg'] == 0:
            answer += (f'Требуются хозяйственные товары для {result["hg_entity"]}'
                       f' к {result["hg_date"]}\n')
        else:
            answer += f'Хозяйственные товары уже подготовлены\n'
        if result["goods_date"] and result['status_goods'] == 0:
            answer += f'Требуется товар к {result["goods_date"]}\n'
        else:
            answer += f'Товар уже подготовлен\n'
        answer += f'Задачу создал @{result["created_task_user"]}\n'
        if user_status in [2, 4, 5, 6]:
            status.update({'status_goods': result['status_goods']})
        if user_status in [3, 4, 7, 8]:
            status.update({'status_hg': result['status_hg']})

        return answer, status, None, result['created_task_user']
    elif table == 'info':
        result = session.query(info_open).where(info_open.c.id == task_id).all()[0]
        answer = (f'{result["address"]} будет открыт '
                  f'{result["date"]}.\n'
                  f'Координаты магазина: {result["coordinates"]}\n'
                  f'График работы: {result["schedule"]}\n'
                  f'Описание: {result["description"]}\n\n')
        if result["entity"] and result["area"]:
            answer += (f'Данные для QR кода:\n'
                      f'Юр.лицо:{result["entity"]}\n'
                      f'Площадь торгового зала:{result["area"]}\n')
        if result["passport_1"] and result["snils_1"]:
            answer += (f'Информация о сотруднике:\n'
                       f'Паспорт: {decode_hash(result["passport_1"])}\n'
                       f'СНИЛС: {decode_hash(result["snils_1"])}\n')
        if result["passport_2"] and result["snils_2"]:
            answer += (f'Информация о сотруднике:\n'
                       f'Паспорт: {decode_hash(result["passport_2"])}\n'
                       f'СНИЛС: {decode_hash(result["snils_2"])}\n')
        if result["photo_markup"] and result["photo_screen"] and result["photo_household"]:
            photo = [result["photo_markup"], result["photo_screen"], result["photo_household"]]
            answer += f'Задачу создал @{result["created_task_user"]}\n'
            return answer, result['status'], photo, result['created_task_user']
        answer += f'Задачу создал @{result["created_task_user"]}\n'
        return answer, result['status'], None, result['created_task_user']


async def change_task_query(table, task_id, status, user_name=None, status_name=None):
    if table == 'technique':
        session.query(technique).where(technique.c.id == task_id).update({'status': status,
                                                                          'closed_task_user': user_name})
        session.commit()
    elif table == 'new_shop':
        session.query(new_shop).where(new_shop.c.id == task_id).update({status_name: status,
                                                                        'closed_task_hg_user': user_name})
        session.commit()
    elif table == 'info':
        session.query(info_open).where(info_open.c.id == task_id).update({'status': status,
                                                                          'closed_task_user': user_name})
        session.commit()

