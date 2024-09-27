from aiogram_dialog import DialogManager
from bot.db.requests import get_userlist_db, get_tasks_count_db


async def getter_of_userlist(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    raw_userlist = await get_userlist_db(session)
    result_userlist = [
        (f"{user_id}, {first_name}, {username}", None)
        for user_id, first_name, username in raw_userlist
    ]
    return {
        "users": result_userlist,
    }


async def getter_of_task_count(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session")
    task_count = await get_tasks_count_db(session)
    return {
        "count": task_count,
    }
