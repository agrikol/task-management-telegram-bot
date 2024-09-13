from operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    SwitchTo,
    Row,
    Button,
    Cancel,
    Select,
    ScrollingGroup,
    Back,
)
from bot.states.states import ShowTasksSG
from bot.dialogs.get_tasks.handlers import listing_tasks, edit_task
from bot.dialogs.get_tasks.getters import getter_of_names, getter_of_task


task_list_dialog = Dialog(
    Window(
        Const("Ваши задачи:"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="task",
                item_id_getter=itemgetter(
                    1
                ),  # TODO: emoji for irrelevant tasks + sort by date
                items="task_names",
                on_click=listing_tasks,
            ),
            width=1,
            height=5,
            id="task_list",
        ),
        Cancel(Const("« Назад"), id="cancel"),
        state=ShowTasksSG.start,
        getter=getter_of_names,
    ),
    Window(
        Format(
            "Имя задачи: <code>{name}</code>\
            \nОписание: {desc}\nКатегория: {categ}\nСрок: {due}\
            \nНапоминание: {notice}"
        ),
        Row(
            SwitchTo(Const("Имя"), id="name", state=ShowTasksSG.name),
            SwitchTo(Const("Описание"), id="desc", state=ShowTasksSG.desc),
        ),
        Row(
            SwitchTo(Const("Категория"), id="categ", state=ShowTasksSG.categ),
            SwitchTo(Const("Срок"), id="due", state=ShowTasksSG.due),
        ),
        SwitchTo(Const("Напоминание"), id="notice", state=ShowTasksSG.notice),
        Row(
            Button(
                Const("☑️ Сохранить"),
                id="save",
                on_click=edit_task,
            ),
            Button(Const("❌ Удалить"), id="delete", on_click=edit_task),
            Button(Const("✅ Выполнено"), id="done", on_click=edit_task),
        ),
        Back(Const("« Назад"), id="back"),
        state=ShowTasksSG.task_edit,
        getter=getter_of_task,
    ),
)
