from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopFSMAdmin(StatesGroup):
    name = State()
    photo = State()
    prise = State()
    category = State()