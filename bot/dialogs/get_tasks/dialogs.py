from operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from bot.dialogs.create_task.getters import get_hours, get_minutes, get_notice
from bot.dialogs.create_task.handlers import clear_hours
from aiogram_dialog.widgets.kbd import (
    SwitchTo,
    Row,
    Button,
    Cancel,
    Select,
    ScrollingGroup,
    Back,
    Group,
    Calendar,
)
from bot.states.states import EditTasksSG
from bot.dialogs.get_tasks.handlers import (
    listing_tasks,
    edit_task,
    edit_name_handler,
    edit_desc_handler,
    edit_tag,
    edit_date,
    edit_hour,
    save_due_edit,
    skip_hours,
    edit_notice,
    delete_task,
    complete_task,
)
from bot.dialogs.get_tasks.getters import (
    getter_of_names,
    getter_of_task,
    getter_of_tag,
)


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
            hide_on_single_page=True,
        ),
        Cancel(Const("☰ Меню"), id="cancel"),
        state=EditTasksSG.start,
        getter=getter_of_names,
    ),
    Window(
        Format(
            "Имя задачи: <code>{name}</code>\
            \nОписание: <code>{desc}</code>\nТэг: {tag}\nСрок: {due}\
            \nНапоминание: {notice}"
        ),
        Row(
            SwitchTo(Const("Имя"), id="name", state=EditTasksSG.name),
            SwitchTo(Const("Описание"), id="desc", state=EditTasksSG.desc),
        ),
        Row(
            SwitchTo(Const("Тэг"), id="tag", state=EditTasksSG.tag),
            SwitchTo(Const("Срок"), id="due", state=EditTasksSG.due),
        ),
        SwitchTo(
            Const("Напоминание"), id="notice", state=EditTasksSG.notice, when="is_time"
        ),
        Row(
            Button(Const("❌ Удалить"), id="delete", on_click=delete_task),
            Button(
                Const("☑️ Сохранить"),
                id="save",
                on_click=edit_task,
            ),
            Button(Const("✅ Выполнено"), id="done", on_click=complete_task),
        ),
        Back(Const("« Назад"), id="to_list"),
        state=EditTasksSG.task_edit,
        getter=getter_of_task,
    ),
    Window(
        Const("Введите новое имя задачи:"),
        TextInput(
            id="edit_name",
            on_success=edit_name_handler,
        ),
        SwitchTo(Const("« Назад"), id="to_edit", state=EditTasksSG.task_edit),
        state=EditTasksSG.name,
    ),
    Window(
        Const("Введите новое описание задачи:"),
        TextInput(id="edit_desc", on_success=edit_desc_handler),
        SwitchTo(Const("« Назад"), id="to_edit", state=EditTasksSG.task_edit),
        state=EditTasksSG.desc,
    ),
    Window(
        Const("Выберите тэг:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="tag",
                item_id_getter=itemgetter(1),
                items="tags",
                on_click=edit_tag,
            ),
            width=1,
        ),
        SwitchTo(Const("« Назад"), id="to_edit", state=EditTasksSG.task_edit),
        state=EditTasksSG.tag,
        getter=getter_of_tag,
    ),
    Window(
        Const("Выберите дату:"),
        Calendar(id="edit_date", on_click=edit_date),
        SwitchTo(Const("« Назад"), id="to_edit", state=EditTasksSG.task_edit),
        state=EditTasksSG.due,
    ),
    Window(
        Const("Выберите час:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="time",
                item_id_getter=lambda x: x[1],
                items="time_list",
                on_click=edit_hour,
            ),
            width=6,
        ),
        SwitchTo(
            Const("Пропустить »"),
            id="skip_time",
            state=EditTasksSG.task_edit,
            on_click=skip_hours,
        ),
        Back(Const("« Назад"), id="to_edit_date"),
        getter=get_hours,
        state=EditTasksSG.due_hour,
    ),
    Window(
        Const("Выберите минуты:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="time",
                item_id_getter=lambda x: x[1],
                items="time_list",
                on_click=save_due_edit,
            ),
            width=6,
        ),
        Back(
            Const("« Назад"),
            id="to_edit_hour",
            on_click=clear_hours,
        ),
        getter=get_minutes,
        state=EditTasksSG.due_minute,
    ),
    Window(
        Const("Когда прислать напоминание?"),  # TODO: Checkbox
        Group(
            Select(
                Format("{item[0]}"),
                id="notice",
                item_id_getter=lambda x: x[1],
                items="notice_list",
                on_click=edit_notice,
            ),
            width=4,
        ),
        SwitchTo(Const("« Назад"), id="to_edit", state=EditTasksSG.task_edit),
        state=EditTasksSG.notice,
        getter=get_notice,
    ),
)
