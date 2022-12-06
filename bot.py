from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()

# TOKEN = "5812120409:AAFUcV6Grc9KcJS-slCNJYukzhRjoi9-iD4"
TOKEN = '5657011402:AAFRTPDQMEPTwHWF40ME4NLD9D5ivmtRVkg'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
