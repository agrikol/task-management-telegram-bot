from aiogram import Bot
from bot.kb.notice_kb import notice_kb
from bot.db.requests import get_task_short_info
from sqlalchemy.ext.asyncio import async_sessionmaker


async def send_notice(
    bot: Bot, chat_id: int, task_id: int, session: async_sessionmaker
) -> None:
    async with session() as session:
        task_name, task_desc = await get_task_short_info(
            session=session, task_id=int(task_id)
        )

    text: str = f"Уведомление\n\nЗадача: {task_name}\nОписание: {task_desc}"
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=notice_kb(task_id=task_id),
    )
