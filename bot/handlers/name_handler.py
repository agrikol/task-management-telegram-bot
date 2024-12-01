from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager
from bot.states.states import CreateTaskSG
from bot.filters.dialog_filters import DialogGroupFilter, DialogFilter
from aiogram_dialog.api.entities import ShowMode


task_name_router: Router = Router()


@task_name_router.message(F.text, ~DialogGroupFilter(CreateTaskSG))
async def process_create_task_with_name(
    message: Message, dialog_manager: DialogManager
):
    name, *desc = message.text.split("\n", 1)
    data = {"name": name, "desc": desc[0]} if desc else {"name": name}
    await message.delete()
    await dialog_manager.start(CreateTaskSG.start, data=data, show_mode=ShowMode.EDIT)
