from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import or_f
from aiogram_dialog import DialogManager
from bot.states.states import (
    CreateTaskSG,
    EditTasksSG,
    NoticeEditSG,
    FeedbackSG,
    AdminSG,
)
from bot.filters.dialog_filters import DialogGroupFilter
from aiogram_dialog.api.entities import ShowMode


task_name_router: Router = Router()


@task_name_router.message(
    F.text,
    ~or_f(
        DialogGroupFilter(CreateTaskSG),
        DialogGroupFilter(EditTasksSG),
        DialogGroupFilter(NoticeEditSG),
        DialogGroupFilter(FeedbackSG),
        DialogGroupFilter(AdminSG),
    ),
)
async def process_create_task_with_name(
    message: Message, dialog_manager: DialogManager
):
    name, *desc = message.text.split("\n", 1)
    data = {"name": name, "desc": desc[0]} if desc else {"name": name}
    await message.delete()
    await dialog_manager.start(CreateTaskSG.start, data=data, show_mode=ShowMode.EDIT)
