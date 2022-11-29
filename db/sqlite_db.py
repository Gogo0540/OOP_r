import sqlite3


def sql_start():
    global base, cursor
    base = sqlite3.connect('db.sqlite3')
    cursor = base.cursor()
    if base:
        print('Database connected')
        base.execute(
            'CREATE TABLE IF NOT EXISTS student(name TEXT PRIMARY KEY, photo TEXT, course TEXT)'
        )

        base.execute(
            'CREATE TABLE IF NOT EXISTS course(name TEXT PRIMARY KEY)'
        )
        base.execute(
            'CREATE TABLE IF NOT EXISTS shop(name TEXT PRIMARY KEY, photo TEXT, prise DOUBLE, category TEXT)'
        )
        base.commit()


async def sql_add_command(state, table):
    if table == 'student':
        insert_query = f'INSERT INTO {table} VALUES (?, ?, ?)'
    elif table == 'course':
        insert_query = f'INSERT INTO {table} VALUES (?)'
    elif table == 'shop':
        insert_query = f'INSERT INTO {table} VALUES (?, ?, ?, ?)'

    async with state.proxy() as data:
        cursor.execute(
            insert_query, tuple(data.values())
        )
        base.commit()


async def sql_get_category_command(category):
    select_query = f'SELECT * FROM shop WHERE category = ?'

    return cursor.execute(select_query, (category,))
