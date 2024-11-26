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
    Select,
    Back,
    Group,
    Calendar,
)
from bot.states.states import NoticeEditSG
from bot.dialogs.notification.handlers import (
    edit_notice,
    edit_name_handler,
    edit_desc_handler,
    edit_tag,
    edit_date,
    edit_hour,
    save_due_edit,
    skip_hours,
    edit_notice_time,
    delete_task,
    complete_task,
)
from bot.dialogs.notification.getters import (
    getter_of_task,
    getter_of_tag,
)
from bot.dialogs.notification.handlers import edit_notice


notice_edit_dialog = Dialog(
    Window(
        Format(
            "Имя задачи: <code>{name}</code>\
            \nОписание: <code>{desc}</code>\nТэг: {tag}\nСрок: {due}\
            \nНапоминание: {notice}"
        ),
        Row(
            SwitchTo(Const("Имя"), id="name", state=NoticeEditSG.name),
            SwitchTo(Const("Описание"), id="desc", state=NoticeEditSG.desc),
        ),
        Row(
            SwitchTo(Const("Тэг"), id="tag", state=NoticeEditSG.tag),
            SwitchTo(Const("Срок"), id="due", state=NoticeEditSG.due),
        ),
        SwitchTo(
            Const("Напоминание"), id="notice", state=NoticeEditSG.notice, when="is_time"
        ),
        Row(
            Button(Const("❌ Удалить"), id="delete", on_click=delete_task),
            Button(
                Const("☑️ Сохранить"),
                id="save",
                on_click=edit_notice,
            ),
            Button(Const("✅ Выполнено"), id="done", on_click=complete_task),
        ),
        state=NoticeEditSG.start,
        getter=getter_of_task,
    ),
    Window(
        Const("Введите новое имя задачи:"),
        TextInput(
            id="edit_name",
            on_success=edit_name_handler,
        ),
        SwitchTo(Const("« Назад"), id="to_edit", state=NoticeEditSG.start),
        state=NoticeEditSG.name,
    ),
    Window(
        Const("Введите новое описание задачи:"),
        TextInput(id="edit_desc", on_success=edit_desc_handler),
        SwitchTo(Const("« Назад"), id="to_edit", state=NoticeEditSG.start),
        state=NoticeEditSG.desc,
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
        SwitchTo(Const("« Назад"), id="to_edit", state=NoticeEditSG.start),
        state=NoticeEditSG.tag,
        getter=getter_of_tag,
    ),
    Window(
        Const("Выберите дату:"),
        Calendar(id="edit_date", on_click=edit_date),
        SwitchTo(Const("« Назад"), id="to_edit", state=NoticeEditSG.start),
        state=NoticeEditSG.due,
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
            state=NoticeEditSG.start,
            on_click=skip_hours,
        ),
        Back(Const("« Назад"), id="to_edit_date"),
        getter=get_hours,
        state=NoticeEditSG.due_hour,
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
        state=NoticeEditSG.due_minute,
    ),
    Window(
        Const("Когда прислать напоминание?"),  # TODO: Checkbox
        Group(
            Select(
                Format("{item[0]}"),
                id="notice",
                item_id_getter=lambda x: x[1],
                items="notice_list",
                on_click=edit_notice_time,
            ),
            width=4,
        ),
        SwitchTo(Const("« Назад"), id="to_edit", state=NoticeEditSG.start),
        state=NoticeEditSG.notice,
        getter=get_notice,
    ),
)
