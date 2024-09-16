from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from bot.states.states import CreateTaskSG, ShowTasksSG
from bot.db.requests import get_tasks_names


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
) -> None:
    session = manager.middleware_data.get("session")
    names = await get_tasks_names(session, callback.from_user.id)
    names = [(i, str(j)) for i, j in names]
    await manager.start(ShowTasksSG.start, data={"task_names": names})
