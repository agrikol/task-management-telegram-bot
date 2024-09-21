from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from bot.states.states import StartSG, AdminSG


admin_dialog = Dialog(
    Window(
        Const("👨‍💻 Админ панель"),
        Button(Const("⚙ Настройки"), id="settings"),
        state=AdminSG.start,
    ),
)
