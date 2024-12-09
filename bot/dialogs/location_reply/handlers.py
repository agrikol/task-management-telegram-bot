from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal.fake_data import ReplyCallbackQuery


async def del_msg(
    message: ReplyCallbackQuery,
    _,
    dialog_manager: DialogManager,
):
    await message.original_message.delete()
