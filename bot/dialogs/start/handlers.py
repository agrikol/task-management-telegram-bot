from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from states.states import NewTaskSG, ShowTaskSG


async def create_task(
    dialog_manager: DialogManager, callback: CallbackQuery
) -> None:
    await dialog_manager.start(NewTaskSG.start)


async def show_tasks(
    dialog_manager: DialogManager, callback: CallbackQuery
) -> None:
    await dialog_manager.start(ShowTaskSG.start)