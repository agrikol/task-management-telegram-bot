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
)
from bot.states.states import CreateTaskSG
from bot.dialogs.create_task.getters import get_name, get_hours, get_minutes, get_notice
from bot.dialogs.create_task.handlers import (
    add_desc_handler,
    add_name_handler,
    add_category,
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
            \nОписание: {desc}\nКатегория: {categ}\nСрок: {due}\
            \nНапоминание: {notice}"
        ),
        Row(
            SwitchTo(Const("Имя"), id="name", state=CreateTaskSG.name),
            SwitchTo(Const("Описание"), id="desc", state=CreateTaskSG.desc),
        ),
        Row(
            SwitchTo(Const("Категория"), id="categ", state=CreateTaskSG.categ),
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
        getter=get_name,
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
        SwitchTo(Const("« Назад"), id="cancel", state=CreateTaskSG.due),
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
        SwitchTo(
            Const("« Назад"),
            id="cancel",
            state=CreateTaskSG.due_hour,
            on_click=clear_hours,
        ),
        getter=get_minutes,
        state=CreateTaskSG.due_minute,
    ),
    Window(
        Const("Выберите категорию:"),
        Row(
            SwitchTo(
                Const("🔴 Красная"),
                id="category_1",
                state=CreateTaskSG.start,
                on_click=add_category,
            ),
            SwitchTo(
                Const("🟡 Желтая"),
                id="category_2",
                state=CreateTaskSG.start,
                on_click=add_category,
            ),
        ),
        Row(
            SwitchTo(
                Const("🟢 Зеленая"),
                id="category_3",
                state=CreateTaskSG.start,
                on_click=add_category,
            ),
            SwitchTo(
                Const("🔵 Синяя"),
                id="category_4",
                state=CreateTaskSG.start,
                on_click=add_category,
            ),
        ),
        SwitchTo(Const("« Назад"), id="cancel", state=CreateTaskSG.start),
        state=CreateTaskSG.categ,
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
