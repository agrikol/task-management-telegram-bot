from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    # admin = State()


class AdminSG(StatesGroup):
    start = State()
    userlist = State()
    task_count = State()


class CreateTaskSG(StatesGroup):
    start = State()
    name = State()
    desc = State()
    tag = State()
    tag_list = State()
    due = State()
    due_hour = State()
    due_minute = State()
    notice = State()
    save = State()


class ShowTasksSG(StatesGroup):
    start = State()
    task_edit = State()
    task_edited = State()
    name = State()
    desc = State()
    tag = State()
    tag_list = State()
    due = State()
    due_hour = State()
    due_minute = State()
    notice = State()
    save = State()
    delete = State()


class TodayTasksSG(StatesGroup):
    start = State()


class HelpSG(StatesGroup):
    start = State()


class FeedbackSG(StatesGroup):
    start = State()
    feedback = State()
    bug_report = State()
