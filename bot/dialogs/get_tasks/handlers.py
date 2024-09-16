from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select
from bot.states.states import ShowTasksSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.requests import add_task, get_task_info
from bot.db.models import Task


async def listing_tasks(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    *args,
    **kwargs,
):
    session: AsyncSession = manager.middleware_data.get("session")
    task: Task = await get_task_info(session, int(callback.data.split(":")[1]))
    manager.dialog_data.update(task.to_dict())
    await manager.switch_to(ShowTasksSG.task_edit)


async def edit_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    data: dict = manager.dialog_data
    session: AsyncSession = manager.middleware_data.get("session")
    await add_task(
        session,
        user_id=callback.from_user.id,
        name=data.get("name"),
        desc=data.get("desc"),
        categ=data.get("categ"),
        due=data.get("due") + " " + data.get("time"),
        notice=data.get("notice"),
    )
    await callback.answer("✅ Задача сохранена")
    await manager.done()


async def edit_name_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(name=text)
    await manager.switch_to(ShowTasksSG.task_edit)


async def edit_desc_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(desc=text)
    await manager.switch_to(ShowTasksSG.task_edit)


async def edit_category(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
    *args,
) -> None:
    manager.dialog_data.update(categ=callback.data.split(":")[1])
    await manager.switch_to(ShowTasksSG.task_edit)
