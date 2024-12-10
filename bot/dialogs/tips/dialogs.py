from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import (
    Row,
    Start,
    Back,
    Next,
)
from bot.states.states import TipsSG, LocationSG, StartSG
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType


tips_dialog = Dialog(
    Window(
        Const("💡 <b>Tip #1</b>"),
        Const(
            "Для того, чтобы сервис смог отправлять вам уведомления в корректное время - "
            "нужно указать часовой пояс, в котором вы находитесь."
        ),
        Start(Const("Указать часовой пояс"), id="timezone", state=LocationSG.MAIN),
        Row(
            Start(Const("☰ Меню"), id="to_menu", state=StartSG.start),
            Next(Const("Далее »"), id="next"),
        ),
        state=TipsSG.FIRST,
    ),
    Window(
        Const("💡 <b>Tip #2</b>"),
        Const("Просмотрите короткий GIF-ролик о способах создать задачу"),
        StaticMedia(
            path=r"bot/media/1.gif",
            type=ContentType.ANIMATION,
        ),
        Row(
            Back(Const("« Назад"), id="back"),
            Start(Const("☰ Меню"), id="to_menu", state=StartSG.start),
            Next(Const("Далее »"), id="next"),
        ),
        state=TipsSG.SECOND,
    ),
    Window(
        Const("💡 <b>Tip #3</b>"),
        Const("Посмотрите короткий GIF-ролик о том, как работают Напоминания"),
        StaticMedia(
            path=r"bot/media/2.gif",
            type=ContentType.ANIMATION,
        ),
        Row(
            Back(Const("« Назад"), id="back"),
            Start(Const("☰ Меню"), id="to_menu", state=StartSG.start),
            Next(Const("Далее »"), id="next"),
        ),
        state=TipsSG.THIRD,
    ),
    Window(
        Const("💡 <b>Tip #4</b>"),
        Const(
            "Если вы столкнулись с ошибкой или неожиданным поведением сервиса - "
            "просто нажмите /start, чтобы вернуться в ☰ Меню.\n\n"
            "Если ошибка сохраняется - обязательно воспользуйтесь командой /feedback"
        ),
        StaticMedia(
            path=r"bot/media/3.gif",
            type=ContentType.ANIMATION,
        ),
        Row(
            Back(Const("« Назад"), id="back"),
            Start(Const("☰ Меню"), id="to_menu", state=StartSG.start),
        ),
        state=TipsSG.FOURTH,
    ),
)
