from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import RequestLocation, Row, Button
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format
from bot.states.states import LocationSG

reply_kbd_dialog = Dialog(
    Window(
        Const(
            "Нажмите на 📍. Бот не будет хранить ваше местоположение и "
            "использует его один раз только для определения часового пояса\n"
            "\nНажмите 🚫 для отмены"
        ),
        Row(
            Button(Const("🚫"), id="cncl"),
            RequestLocation(Const("📍")),
        ),
        markup_factory=ReplyKeyboardFactory(
            input_field_placeholder=Format("{event.from_user.username}"),
            resize_keyboard=True,
        ),
        state=LocationSG.MAIN,
    ),
)
