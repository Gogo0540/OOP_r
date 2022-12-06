import sqlite3


def sql_start():
    global base, cursor
    base = sqlite3.connect('db.sqlite3')
    cursor = base.cursor()
    if base:
        print('Database connected')
        base.execute('CREATE TABLE IF NOT EXISTS category(category_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        base.commit()
        base.execute(
            'CREATE TABLE IF NOT EXISTS shop('
            'name TEXT PRIMARY KEY,'
            'photo TEXT, prise DOUBLE,'
            'category_id INTEGER,'
            'FOREIGN KEY (category_id)'
            'REFERENCES category(category_id)'
            ')'
        )
        base.commit()


async def sql_add_command(state, table):
    if table == 'shop':
        insert_query = f'INSERT INTO {table} VALUES (?, ?, ?, ?)'
    if table == 'category':
        insert_query = f'INSERT INTO category(name) VALUES (?)'
    async with state.proxy() as data:
        cursor.execute(
            insert_query, tuple(data.values())
        )
        base.commit()


async def sql_get_category_command(category_id):
    select_query = f'SELECT * FROM shop WHERE category_id = ?'

    return cursor.execute(select_query, (category_id,))


async def sql_get_category_names():
    select_query = f'SELECT * FROM category'

    return cursor.execute(select_query)


async def sql_get_category_by_id(id):
    return cursor.execute('SELECT * FROM category')
