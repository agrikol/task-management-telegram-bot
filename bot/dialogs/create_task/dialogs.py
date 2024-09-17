from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Row,
    Cancel,
    SwitchTo,
    Calendar,
    Select,
    Group,
    Button,
    Back,
)
from bot.states.states import CreateTaskSG
from bot.dialogs.create_task.getters import (
    get_template,
    get_hours,
    get_minutes,
    get_notice,
)
from bot.dialogs.create_task.handlers import (
    add_desc_handler,
    add_name_handler,
    add_tag,
    select_date,
    select_hour,
    save_due,
    save_notice,
    save_task,
    clear_hours,
)


create_task_dialog = Dialog(
    Window(
        Format(
            "Имя задачи: <code>{name}</code>\
            \nОписание: {desc}\nТэг: {tag}\nСрок: {due}\
            \nНапоминание: {notice}"
        ),
        Row(
            SwitchTo(Const("Имя"), id="name", state=CreateTaskSG.name),
            SwitchTo(Const("Описание"), id="desc", state=CreateTaskSG.desc),
        ),
        Row(
            SwitchTo(Const("Тэг"), id="tag", state=CreateTaskSG.tag),
            SwitchTo(Const("Срок"), id="due", state=CreateTaskSG.due),
        ),
        SwitchTo(Const("Напоминание"), id="notice", state=CreateTaskSG.notice),
        Button(
            Const("☑️ Сохранить"),
            id="save",
            on_click=save_task,
        ),
        Cancel(Const("« Назад"), id="calcel"),
        state=CreateTaskSG.start,
        getter=get_template,
    ),
    Window(
        Const("Введите имя задачи:"),
        TextInput(
            id="add_name",
            on_success=add_name_handler,
        ),
        state=CreateTaskSG.name,
    ),
    Window(
        Const("Введите описание задачи:"),
        TextInput(id="add_desc", on_success=add_desc_handler),
        state=CreateTaskSG.desc,
    ),
    Window(
        Const("Выберите дату:"),
        Calendar(id="date", on_click=select_date),
        SwitchTo(Const("« Назад"), id="cancel", state=CreateTaskSG.start),
        state=CreateTaskSG.due,
    ),
    Window(
        Const("Выберите час:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="time",
                item_id_getter=lambda x: x[1],
                items="time_list",
                on_click=select_hour,
            ),
            width=6,
        ),
        SwitchTo(
            Const("Пропустить »"),
            id="cancel",
            state=CreateTaskSG.start,
            on_click=clear_hours,
        ),
        Back(Const("« Назад"), id="to_date"),
        getter=get_hours,
        state=CreateTaskSG.due_hour,
    ),
    Window(
        Const("Выберите минуты:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="time",
                item_id_getter=lambda x: x[1],
                items="time_list",
                on_click=save_due,
            ),
            width=6,
        ),
        Back(
            Const("« Назад"),
            id="to_hours",
            on_click=clear_hours,
        ),
        getter=get_minutes,
        state=CreateTaskSG.due_minute,
    ),
    Window(
        Const("Выберите тэг:"),
        Row(
            SwitchTo(
                Const("🔴"),  # TODO: Switch to Select
                id="1",
                state=CreateTaskSG.start,
                on_click=add_tag,
            ),
            SwitchTo(
                Const("🟡"),
                id="2",
                state=CreateTaskSG.start,
                on_click=add_tag,
            ),
        ),
        Row(
            SwitchTo(
                Const("🟢"),
                id="3",
                state=CreateTaskSG.start,
                on_click=add_tag,
            ),
            SwitchTo(
                Const("🔵"),
                id="4",
                state=CreateTaskSG.start,
                on_click=add_tag,
            ),
        ),
        SwitchTo(Const("« Назад"), id="cancel", state=CreateTaskSG.start),
        state=CreateTaskSG.tag,
    ),
    Window(
        Const("Когда прислать напоминание?"),  # TODO: Checkbox
        Group(
            Select(
                Format("{item[0]}"),
                id="notice",
                item_id_getter=lambda x: x[1],
                items="notice_list",
                on_click=save_notice,
            ),
            width=4,
        ),
        SwitchTo(Const("« Назад"), id="cancel", state=CreateTaskSG.start),
        state=CreateTaskSG.notice,
        getter=get_notice,
    ),
)
