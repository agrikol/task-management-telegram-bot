from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Text
from bot.states.states import FeedbackSG


async def accept_feedback(
    callback: CallbackQuery, widget: TextInput, manager: DialogManager, text: Text
):
    bot: Bot = manager.middleware_data["bot"]
    # TODO send message to admin
    try:
        await bot.delete_messages(
            callback.message.chat.id,
            [callback.message.message_id - 1, callback.message.message_id],
        )
    except Exception as e:
        pass  # TODO add logger
    await callback.answer("✅ Спасибо за ваш отзыв")
    await manager.done()
