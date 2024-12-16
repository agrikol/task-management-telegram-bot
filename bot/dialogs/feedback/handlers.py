import logging
import asyncio
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Text
from bot.states.states import FeedbackSG
from aiogram_dialog.api.entities import ShowMode


logger = logging.getLogger(__name__)


async def move_to_bug_report(
    callback: CallbackQuery, widget: TextInput, manager: DialogManager
):
    manager.dialog_data.update(feedback_type=callback.data)
    await manager.switch_to(FeedbackSG.bug_report, show_mode=ShowMode.EDIT)


async def move_to_feedback(
    callback: CallbackQuery, widget: TextInput, manager: DialogManager
):
    manager.dialog_data.update(feedback_type=callback.data)
    await manager.switch_to(FeedbackSG.feedback, show_mode=ShowMode.EDIT)


async def accept_feedback(  # TODO: save to some storage
    message: Message, widget: TextInput, manager: DialogManager, text: Text
):
    bot: Bot = manager.middleware_data["bot"]
    admin_ids: list = manager.middleware_data["admin_ids"]
    feedack_type: str = manager.dialog_data.get("feedback_type")
    text: str = (
        f"{feedack_type}\n{message.from_user.username}\n{message.from_user.id}:\n{text}"
    )
    await message.delete()
    try:
        await asyncio.gather(  # TODO: NATS
            *(
                bot.send_message(admin_id, text)
                for admin_id in admin_ids
                if admin_id != message.from_user.id
            )
        )

    except Exception as e:
        logger.error(e)

    await manager.done(show_mode=ShowMode.EDIT)
