from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Case, Const, List
from aiogram_dialog.widgets.kbd import Button, Row, Start
from bot.states.states import StartSG, CreateTaskSG, ShowTasksSG
from bot.dialogs.start.getters import get_name
from bot.dialogs.start.handlers import start_create_task, start_get_tasks


start_dialog = Dialog(
    Window(
        Format("Приветствую в <code>BotName</code>, {name}! Начнем планирование?"),
        Row(
            Button(Const("Создать задачу"), id="new_task", on_click=start_create_task),
            Button(Const("Мои задачи"), id="my_tasks", on_click=start_get_tasks),
        ),
        state=StartSG.start,
        getter=get_name,
    )
)
