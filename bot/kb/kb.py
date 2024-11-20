from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def notice_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text="Показать",
            callback_data="show",
        ),
        InlineKeyboardButton(
            text="Удалить",
            callback_data="delete",
        ),
    ]

    builder.add(*btns)
    return builder.as_markup()
