from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import dp, bot

from states.students import StudentFSMAdmin, CourseFSMAdmin
from db import sqlite_db
from keyboards.client.admin import student_keyboard


ID = None


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, "choose action: ", reply_markup=student_keyboard
    )
    await message.delete()


async def create_student(message: types.Message):
    if message.from_user.id == ID:
        await StudentFSMAdmin.name.set()
        await message.answer('Send your name')
    await message.answer('You are not an admin')


# @dp.message_handler(state="*", commands="cancel")
# @dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if message.from_user.id == ID:
        if current_state is None:
            return
        await state.finish()
        await message.answer("canceled")


async def set_student_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:    
        async with state.proxy() as data:
            data['name'] = message.text
        await StudentFSMAdmin.next()
        await message.answer('Send your photo')


async def set_student_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await StudentFSMAdmin.next()
        await message.answer('Выберите курс (Python, JavaScript, etc..)')


async def set_student_course(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:        
        async with state.proxy() as data:
            data['course'] = message.text

        await sqlite_db.sql_add_command(state, 'student')
        await state.finish()
        await message.answer('Готово')


async def get_students_list(message: types.Message):
    for obj in sqlite_db.cursor.execute('SELECT * FROM student').fetchall():
        await bot.send_photo(ID, obj[1], f"name: {obj[0]}\n course: {obj[2]}")


async def create_course(message: types.Message):
    if message.from_user.id == ID:
        await CourseFSMAdmin.name.set()
        await message.answer('Type course: ')


async def set_course_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text.capitalize()
        
        await sqlite_db.sql_add_command(state, 'course')
        await state.finish()
        await message.answer('course created!')


async def get_courses_list(message: types.Message):
    print('-'*80)
    courses_list = ''
    for obj in sqlite_db.cursor.execute('SELECT * FROM course').fetchall():
        courses_list += f' Название курса: {obj[0]}\n'
    
    await message.answer(courses_list)


def register_student_handler(dp: Dispatcher):
    dp.register_message_handler(create_student, commands=['create_student'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(set_student_name, state=StudentFSMAdmin.name)
    dp.register_message_handler(set_student_photo, content_types=['photo'], state=StudentFSMAdmin.photo)
    dp.register_message_handler(set_student_course, state=StudentFSMAdmin.course)
    dp.register_message_handler(get_students_list, commands=['students_list'])
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(create_course, commands=['add_course'])
    dp.register_message_handler(set_course_name, state=CourseFSMAdmin.name)
    dp.register_message_handler(get_courses_list, commands=['courses_list'])
