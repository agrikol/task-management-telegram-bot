from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Case, Const, List
from aiogram_dialog.widgets.kbd import Button, Row
from states.states import StartSG
from dialogs.start.getters import get_name
from dialogs.start.handlers import create_task, show_tasks

start_dialog = Dialog(
    Window(
        Format("Приветствую в <code>BotName</code>, {name}! Начнем планирование?"),
        Row(
            Button(Const("Создать задачу"), id="yes", on_click=create_task),
            Button(Const("Мои задачи"), id="no", on_click=show_tasks),
        ),
        state=StartSG.start,
        getter=get_name,
    )
)