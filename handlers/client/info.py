from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import bot
from db import sqlite_db
from aiogram import types
from keyboards.client.info import client_keyboard


async def start_command(message: Message):
    await message.answer('Choose your next option', reply_markup=client_keyboard)


async def get_address(message: Message):
    await message.answer('Ибраимова 103')


async def get_address_shop(message: Message):
    await message.answer('114 ул. Киевская')


async def get_courses_list(message: Message):
    await message.answer('Python, JavaScript, UI/UX, Android')


async def get_category(message: Message):
    categories = await sqlite_db.sql_get_category_names()
    categories_markup = InlineKeyboardMarkup()
    for cat in categories:
        categories_markup.add(InlineKeyboardButton(cat[1], callback_data=f'cat_button {cat[0]}'))
    await message.answer('Выберите категорию!', reply_markup=categories_markup)


async def get_items_on_category(call: types.CallbackQuery):
    call.data = call.data.replace('cat_button ', '')
    items = await sqlite_db.sql_get_category_command(category_id=int(call.data))
    for item in items:
        await bot.send_photo(call.message.chat.id, photo=item[1], caption=f'{item[0]}\nPrice:{item[2]}')


def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(get_address, commands=['address'])
    dp.register_message_handler(get_address_shop, commands=['address_shop'])
    dp.register_message_handler(get_category, commands=['category'])
    dp.register_callback_query_handler(get_items_on_category)
    # dp.register_message_handler(get_courses_list, commands=['courses_list'])

    # dp.register_message_handler(get_students, commands=['python_students_list'])
