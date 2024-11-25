from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from bot.states.states import CreateTaskSG, EditTasksSG, TodayTasksSG
from bot.db.requests import get_tasks_names
from bot.dialogs.create_task.getters import tags


async def start_create_task(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(CreateTaskSG.start)


async def start_get_tasks(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    *args,
) -> None:
    session = manager.middleware_data.get("session")
    names = []
    if "today" not in callback.data:
        request_result = await get_tasks_names(session, callback.from_user.id)
        for name, tag, date, task_id in request_result:
            date: str = datetime.strftime(date, "%d.%m")
            name = f"{tags[tag] if tag != '0' else ''} {name} [{date}]"
            names.append((name, str(task_id)))
    else:
        request_result = await get_tasks_names(
            session, callback.from_user.id, today=True
        )
        for name, tag, date, task_id in request_result:
            date: str = datetime.strftime(date, "%d.%m")
            name = f"{tags[tag] if tag != '0' else ''} {name}"
            names.append((name, str(task_id)))

    await manager.start(EditTasksSG.start, data={"task_names": names})


# async def start_today_tasks(
#     callback: CallbackQuery,
#     button: Button,
#     manager: DialogManager,
# ) -> None:
#     session = manager.middleware_data.get("session")
#     request_result = await get_tasks_names(session, callback.from_user.id, today=True)
#     names = []
#     for name, tag, date, task_id in request_result:
#         date: str = datetime.strftime(date, "%d.%m")
#         name = f"{tags[tag] if tag != '0' else ''} {name} [{date}]"
#         names.append((name, str(task_id)))

#     await manager.start(ShowTasksSG.start, data={"task_names": names})
