from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# [study_request_course.state in (1, 2, 3, 4)]
# 1 = Python
# 2 = JavaScript
# 3 = Android
# 4 = Swift
# 5 = UI/UX



class StudentFSMAdmin(StatesGroup):
    name = State()
    photo = State()
    course = State()


class CourseFSMAdmin(StatesGroup):
    name = State()