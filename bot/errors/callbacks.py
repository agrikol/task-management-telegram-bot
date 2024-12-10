import logging
from aiogram_dialog import DialogManager
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent


logging.basicConfig(level=logging.INFO)


async def on_outdated_intent(event: ErrorEvent):
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "❗️ Сперва закройте другие активные окна ❗️"
        )


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer("Воспользуйтесь другим активным окном")
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest as e:
                logging.exception("Failed to delete message %s", e)
