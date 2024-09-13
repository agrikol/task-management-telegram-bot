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


async def listing_tasks(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    *args,
    **kwargs,
):
    manager.dialog_data.update(task_id=callback.data)
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
