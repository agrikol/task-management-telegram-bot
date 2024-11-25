from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def notice_kb(task_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text="Редактировать",
            callback_data="notice:edit:" + str(task_id),
        ),
        InlineKeyboardButton(
            text="Перенести на завтра",
            callback_data="notice:tomorrow:" + str(task_id),
        ),
        InlineKeyboardButton(
            text="Удалить уведомление",
            callback_data="notice:delete:" + str(task_id),
        ),
    ]

    builder.add(*btns)
    return builder.as_markup()
