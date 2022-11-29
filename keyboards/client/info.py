from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)


# b1 = KeyboardButton('/address')
adress = KeyboardButton('/address_shop')
category = KeyboardButton('/category')
# b3 = KeyboardButton('/python_students_list')


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# insert by right side
# row as line
client_keyboard.row(adress, category)
# client_keyboard.add(b3)
