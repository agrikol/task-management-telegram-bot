from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, List, Format
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, NumberedPager
from aiogram_dialog.widgets.input import TextInput
from bot.states.states import AdminSG
from bot.dialogs.admin.getters import getter_of_userlist, getter_of_task_count
from bot.dialogs.admin.handlers import exit_admin, send_admin_message


admin_dialog = Dialog(
    Window(
        Const("👨‍💻 Welcome, Admin"),
        SwitchTo(Const("⚙ User List"), id="userlist", state=AdminSG.userlist),
        SwitchTo(Const("⚙ Task Count"), id="tasks_count", state=AdminSG.task_count),
        SwitchTo(Const("⚙ Message"), id="message", state=AdminSG.message),
        Button(Const("❌ Exit"), id="exit", on_click=exit_admin),
        state=AdminSG.start,
    ),
    Window(
        Const("👨‍💻 Userlist"),
        List(
            Format("{pos}. {item[0]}"),
            items="users",
            id="userscroll",
            page_size=10,
        ),
        NumberedPager(scroll="userscroll"),
        Back(Const("« Назад"), id="back"),
        state=AdminSG.userlist,
        getter=getter_of_userlist,
        preview_data=getter_of_userlist,
    ),
    Window(
        Format("👨‍💻 Task Count: {count}"),
        SwitchTo(Const("« Назад"), id="back", state=AdminSG.start),
        state=AdminSG.task_count,
        getter=getter_of_task_count,
    ),
    Window(
        Const("👨‍💻 Message: "),
        TextInput(id="adm_msg", on_success=send_admin_message),
        SwitchTo(Const("« Назад"), id="back_msg", state=AdminSG.start),
        state=AdminSG.message,
    ),
)
