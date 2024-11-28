from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def notice_kb(task_id: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btns: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text="Редактировать",
            callback_data="notice:edit:" + str(task_id),
        ),
        InlineKeyboardButton(
            text="🔜 На завтра",
            callback_data="notice:tomorrow:" + str(task_id),
        ),
        InlineKeyboardButton(
            text="✅ Выполнено",
            callback_data="notice:done:" + str(task_id),
        ),
        InlineKeyboardButton(
            text="❌ Удалить уведомление",
            callback_data="notice:delete:" + str(task_id),
        ),
    ]

    builder.row(*btns, width=1)
    return builder.as_markup()
