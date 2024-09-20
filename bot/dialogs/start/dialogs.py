from operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Select
from bot.states.states import StartSG
from bot.dialogs.start.getters import get_start_data
from bot.dialogs.start.handlers import (
    start_create_task,
    start_get_tasks,
)


start_dialog = Dialog(
    Window(
        Format(
            "🤖 Привет {name}, я - робот <b>MAKE-E</b>!\
            \nНачнем планирование?"
        ),
        Row(
            Button(Const("Создать задачу"), id="new_task", on_click=start_create_task),
            Button(
                Const("Мои задачи"),
                id="my_tasks",
                on_click=start_get_tasks,
                when="is_tasks",
            ),
        ),
        Select(
            Format("{item[0]}"),
            id="today",
            item_id_getter=itemgetter(1),
            items="today_date",
            on_click=start_get_tasks,
            when="is_today",
        ),
        getter=get_start_data,
        state=StartSG.start,
    ),
)
