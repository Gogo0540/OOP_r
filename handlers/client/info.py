from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove


from bot import bot
from keyboards.client.info import client_keyboard


async def start_command(message: Message):
    await message.answer('Choose your next option', reply_markup=client_keyboard)


async def get_address(message: Message):
    await message.answer('Ибраимова 103')



async def get_address_shop(message: Message):
    await message.answer('114 ул. Киевская')


async def get_courses_list(message: Message):
    await message.answer('Python, JavaScript, UI/UX, Android')

async def get_category(message:Message):
    await message.answer(f"1. Бытовая техника /appliances\n"
                         f"2. Телефоны /phones\n"
                         f"3. Гаджеты /gadgets ")

def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(get_address, commands=['address'])
    dp.register_message_handler(get_address_shop, commands=['address_shop'])
    dp.register_message_handler(get_category, commands=['category'])

    # dp.register_message_handler(get_courses_list, commands=['courses_list'])
    
    # dp.register_message_handler(get_students, commands=['python_students_list'])
