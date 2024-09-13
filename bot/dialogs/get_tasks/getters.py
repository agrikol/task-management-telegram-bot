from aiogram_dialog import DialogManager
from aiogram.types import User
from bot.db.requests import get_tasks_names, get_task_info
from bot.db.models import Task
from sqlalchemy.ext.asyncio import AsyncSession


async def getter_of_names(
    dialog_manager: DialogManager, event_from_user: User, **kwargs
):
    session = dialog_manager.middleware_data.get("session")
    task_names = await get_tasks_names(session, event_from_user.id)
    return {"task_names": task_names}


async def getter_of_task(
    dialog_manager: DialogManager, event_from_user: User, **kwargs
):
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    task_id: str = dialog_manager.dialog_data.get("task_id")
    task: Task = await get_task_info(session, int(task_id.split(":")[1]))
    return task.to_dict()
