from db import sqlite_db

from aiogram import executor

from bot import dp
from handlers.client import info
from handlers.student import admin, shop, category


async def on_startup(_):
    print('Bot has started')
    sqlite_db.sql_start()


info.register_client_handler(dp)
shop.register_shop_handler(dp)
category.register_category_handler(dp)

if "__main__" == __name__:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
