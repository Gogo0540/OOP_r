from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import dp, bot
from keyboards.client.info import client_keyboard
from states.students import CategoryFSMAdmin
from db import sqlite_db


async def create_category(message: types.Message):
    await CategoryFSMAdmin.name.set()
    await message.answer('send category name')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('canceled')


async def set_category_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await sqlite_db.sql_add_command(state, 'category')
    await state.finish()
    await message.answer('Готово')


def register_category_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(create_category, commands=['create_category'], state=None)
    dp.register_message_handler(set_category_name, state=CategoryFSMAdmin.name)