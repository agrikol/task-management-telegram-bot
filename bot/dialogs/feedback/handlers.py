from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Text
from bot.states.states import FeedbackSG
from bot.config.config_reader import config


async def move_to_bug_report(
    callback: CallbackQuery, widget: TextInput, manager: DialogManager
):
    manager.dialog_data.update(feedback_type=callback.data)
    await manager.switch_to(FeedbackSG.bug_report)


async def move_to_feedback(
    callback: CallbackQuery, widget: TextInput, manager: DialogManager
):
    manager.dialog_data.update(feedback_type=callback.data)
    await manager.switch_to(FeedbackSG.feedback)


async def accept_feedback(
    message: Message, widget: TextInput, manager: DialogManager, text: Text
):
    bot: Bot = manager.middleware_data["bot"]
    admin_ids: list = config.admin_id
    feedack_type = manager.dialog_data.get("feedback_type")
    try:
        await bot.delete_messages(
            message.chat.id,
            [message.message_id - 1, message.message_id],
        )
        for admin_id in admin_ids:
            await bot.send_message(
                admin_id,
                f"Новый {feedack_type}\nот {message.from_user.full_name} "
                "{message.from_user.id}:\n{text}",
            )
    except Exception as e:
        pass  # TODO add logger
    await message.answer("✅ Спасибо за ваш отзыв")
    await manager.done()
