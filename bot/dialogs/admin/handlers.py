import asyncio
from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from bot.states.states import AdminSG
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.requests import get_userlist_db
from aiogram_dialog.api.entities import ShowMode


async def send_admin_message(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    bot: Bot = manager.middleware_data["bot"]
    session: AsyncSession = manager.middleware_data["session"]
    user_ids: list[int] = [user[0] for user in await get_userlist_db(session=session)]
    await asyncio.gather(
        *(bot.send_message(user_id, text) for user_id in user_ids)
    )  # TODO: NATS
    await manager.switch_to(AdminSG.start, show_mode=ShowMode.EDIT)
