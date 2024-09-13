from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class CreateTaskSG(StatesGroup):
    start = State()
    name = State()
    desc = State()
    categ = State()
    categ_list = State()
    due = State()
    due_hour = State()
    due_minute = State()
    notice = State()
    save = State()


class ShowTasksSG(StatesGroup):
    start = State()
    task_edit = State()
    name = State()
    desc = State()
    categ = State()
    categ_list = State()
    due = State()
    due_hour = State()
    due_minute = State()
    notice = State()
    save = State()
    delete = State()


class HelpSG(StatesGroup):
    start = State()


class FeedbackSG(StatesGroup):
    start = State()
    feedback = State()
    bug_report = State()
