from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class AdminSG(StatesGroup):
    start = State()
    userlist = State()
    task_count = State()
    message = State()


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


class EditTasksSG(StatesGroup):
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


class NoticeEditSG(StatesGroup):
    start = State()
    # task_edited = State()
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


class TipsSG(StatesGroup):
    FIRST = State()
    SECOND = State()
    THIRD = State()
    FOURTH = State()


class FeedbackSG(StatesGroup):
    start = State()
    feedback = State()
    bug_report = State()


class LocationSG(StatesGroup):
    MAIN = State()
