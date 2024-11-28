from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from bot.states.states import CreateTaskSG
from bot.filters.dialog_filters import DialogFilter

name_router: Router = Router()


@name_router.message(F.text, ~DialogFilter(CreateTaskSG.name))
async def process_create_task_with_name(
    message: Message, dialog_manager: DialogManager
):
    name, *desc = message.text.split("\n", 1)
    data = {"name": name, "desc": desc[0]} if desc else {"name": name}
    await dialog_manager.start(CreateTaskSG.start, data=data)
