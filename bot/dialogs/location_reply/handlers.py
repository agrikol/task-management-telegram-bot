from aiogram_dialog.api.internal.fake_data import ReplyCallbackQuery


async def del_msg(
    message: ReplyCallbackQuery,
    *args,
):
    await message.original_message.delete()
