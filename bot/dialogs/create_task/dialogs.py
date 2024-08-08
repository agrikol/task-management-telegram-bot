from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Cancel, SwitchTo, Calendar
from states.states import CreateTaskSG
from dialogs.create_task.handlers import (
    name_check,
    correct_age_handler,
    error_age_handler,
)


create_task_dialog = Dialog(
    Window(
        Const("Создана новая задача"),
        Row(
            SwitchTo(Const("Имя"), id="name", state=CreateTaskSG.name),
            SwitchTo(Const("Описание"), id="desc", state=CreateTaskSG.desc),
        ),
        Row(
            SwitchTo(Const("Категория"), id="categ", state=CreateTaskSG.categ),
            SwitchTo(Const("Срок"), id="due", state=CreateTaskSG.due),
        ),
        SwitchTo(Const("Напоминание"), id="notice", state=CreateTaskSG.notice),
        Cancel(Const("« В меню"), id="cancel"),
        state=CreateTaskSG.start,
    ),
    Window(
        Const("Введите имя задачи"),
        TextInput(
            id="add_name",
            type_factory=name_check,
            on_success=correct_age_handler,
            on_error=error_age_handler,
        ),
        state=CreateTaskSG.name,
    ),
    Window(
        Const("Выберите дату"),
        Calendar(id="date", on_click=lambda x: x),
        state=CreateTaskSG.due,
    ),
)
