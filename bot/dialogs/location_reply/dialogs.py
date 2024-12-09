from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import RequestLocation, Row, Start
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format
from bot.states.states import LocationSG, TipsSG
from bot.dialogs.location_reply.handlers import del_msg

reply_kbd_dialog = Dialog(
    Window(
        Const(
            "Нажмите на 📍. Мы не храним ваше местоположение и "
            "используем его один раз только для определения часового пояса\n"
            "\nНажмите 🚫 для отмены"
        ),
        Row(
            Start(
                text=Const("🚫"),
                id="to_second",
                state=TipsSG.SECOND,
                on_click=del_msg,
            ),
            RequestLocation(Const("📍")),
        ),
        markup_factory=ReplyKeyboardFactory(
            input_field_placeholder=Format("{event.from_user.username}"),
            resize_keyboard=True,
        ),
        state=LocationSG.MAIN,
    ),
)
