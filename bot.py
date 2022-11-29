from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()


bot = Bot(token="5812120409:AAFUcV6Grc9KcJS-slCNJYukzhRjoi9-iD4")
dp = Dispatcher(bot, storage=storage)

