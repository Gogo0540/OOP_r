from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import dp, bot
from keyboards.client.info import client_keyboard
from states.students import ShopFSMAdmin
from db import sqlite_db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
ID = None


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    print(ID)
    await bot.send_message(
        message.from_user.id, "choose action: ", reply_markup=client_keyboard
    )
    await message.delete()


async def create_product(message: types.Message):
    print(ID, message.from_user.id)
    if message.from_user.id == ID:
        await ShopFSMAdmin.name.set()
        await message.answer('Send title product')
    else:
        await message.answer('You are not an admin')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if message.from_user.id == ID:
        if current_state is None:
            return
        await state.finish()
        await message.answer("canceled")


async def set_product_title(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await ShopFSMAdmin.next()
        await message.answer('Send photo product')


async def set_product_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await ShopFSMAdmin.next()
        await message.answer('set product price')


async def set_product_category(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['category_id'] = int(message.text.split('.')[0])
        await sqlite_db.sql_add_command(state, 'shop')
        await state.finish()
        await message.answer('Готово')


async def set_product_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        category_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        categories = await sqlite_db.sql_get_category_names()
        for cat in categories:
            category_markup.add(KeyboardButton(f'{cat[0]}. {cat[1]}'))
        await message.answer('Select Category on product', reply_markup=category_markup)
        await ShopFSMAdmin.next()



def register_shop_handler(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['change'])
    dp.register_message_handler(create_product, commands=['create_product'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(set_product_title, state=ShopFSMAdmin.name)
    dp.register_message_handler(set_product_photo, content_types=['photo'], state=ShopFSMAdmin.photo)
    dp.register_message_handler(set_product_price, state=ShopFSMAdmin.prise)
    dp.register_message_handler(set_product_category, state=ShopFSMAdmin.category)
