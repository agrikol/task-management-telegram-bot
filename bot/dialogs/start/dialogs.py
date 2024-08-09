from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Case, Const, List
from aiogram_dialog.widgets.kbd import Button, Row, Start
from states.states import StartSG, CreateTaskSG, ShowTaskSG
from dialogs.start.getters import get_name
from dialogs.create_task.handlers import start_create_task


start_dialog = Dialog(
    Window(
        Format("Приветствую в <code>BotName</code>, {name}! Начнем планирование?"),
        Row(
            Button(Const("Создать задачу"), id="new_task", on_click=start_create_task),
            Start(Const("Мои задачи"), id="my_tasks", state=ShowTaskSG.start),
        ),
        state=StartSG.start,
        getter=get_name,
    )
)
