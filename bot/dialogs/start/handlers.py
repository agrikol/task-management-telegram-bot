from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from bot.states.states import CreateTaskSG, ShowTasksSG


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
    await manager.start(ShowTasksSG.start)
