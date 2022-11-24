from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)


b1 = KeyboardButton('/address')
# b3 = KeyboardButton('/python_students_list')


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# insert by right side
# row as line
client_keyboard.add(b1)
# client_keyboard.add(b3)
