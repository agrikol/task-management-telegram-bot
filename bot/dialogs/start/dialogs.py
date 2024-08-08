from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Case, Const, List
from aiogram_dialog.widgets.kbd import Button, Row, Start
from states.states import StartSG, CreateTaskSG, ShowTaskSG
from dialogs.start.getters import get_name


start_dialog = Dialog(
    Window(
        Format("Приветствую в <code>BotName</code>, {name}! Начнем планирование?"),
        Row(
            Start(Const("Создать задачу"), id="new_task", state=CreateTaskSG.start),
            Start(Const("Мои задачи"), id="my_tasks", state=ShowTaskSG.start),
        ),
        state=StartSG.start,
        getter=get_name,
    )
)