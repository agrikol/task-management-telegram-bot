from datetime import date
from aiogram.types import User
from aiogram_dialog import DialogManager
from bot.db.requests import check_tasks_exist, get_user_timezone
from sqlalchemy.ext.asyncio import AsyncSession


async def getter_of_start_data(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs,
) -> dict[str, str | list[tuple[str, str]] | bool]:
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    today: date = date.today()
    is_tipped: bool = not bool(await get_user_timezone(session, event_from_user.id))
    formatted_date: str = today.strftime("Сегодня %d.%m")  # TODO: add locale
    tasks, today_tasks = await check_tasks_exist(session, event_from_user.id)
    return {
        "name": event_from_user.full_name or event_from_user.username,
        "today_date": [(formatted_date, str(today))],
        "is_tasks": tasks,
        "is_today": today_tasks,
        "is_tipped": is_tipped,
    }
