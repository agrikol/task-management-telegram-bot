from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class CreateTaskSG(StatesGroup):
    start = State()
    name = State()
    desc = State()
    categ = State()
    due = State()
    notice = State()


class ShowTaskSG(StatesGroup):
    start = State()
