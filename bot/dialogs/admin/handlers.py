import asyncio
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput
from bot.states.states import AdminSG
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.requests import get_userlist_db


async def exit_admin(
    callback: CallbackQuery, widget: Button, manager: DialogManager
) -> None:
    await manager.done()


async def send_admin_message(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    bot: Bot = manager.middleware_data["bot"]
    session: AsyncSession = manager.middleware_data["session"]
    await bot.delete_messages(
        message.chat.id, [message.message_id - 1, message.message_id]
    )
    user_ids: list[int] = [user[0] for user in await get_userlist_db(session=session)]
    await asyncio.gather(*(bot.send_message(user_id, text) for user_id in user_ids))
    await manager.switch_to(AdminSG.start)
