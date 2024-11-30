from bot.db.models import Task
from operator import itemgetter
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select
from bot.states.states import EditTasksSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_dialog.api.entities import ShowMode
from bot.db.requests import (
    update_task,
    get_task_info,
    change_status_db,
)


async def listing_tasks(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    *args,
    **kwargs,
):
    session: AsyncSession = manager.middleware_data.get("session")
    task_id = int(callback.data.split(":")[1])
    task: Task = await get_task_info(session, task_id)
    task: dict = task.to_dict()
    task["date"] = task["date"].strftime("%d.%m.%Y")
    task["time"] = task["time"].strftime("%H:%M") if task["time"] else ""
    task["notice"] = (
        datetime.strftime(task["notice"], "%d.%m.%Y %H:%M")
        if task.get("notice")
        else None
    )
    manager.dialog_data.update({**task, "task_id": task_id})
    await manager.switch_to(EditTasksSG.task_edit)


async def edit_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    data: dict = manager.dialog_data
    session: AsyncSession = manager.middleware_data.get("session")
    _date = datetime.strptime(data.get("date"), "%d.%m.%Y").date()
    _time = (
        datetime.strptime(data.get("time"), "%H:%M").time()
        if data.get("time")
        else None
    )
    notice = (
        datetime.strptime(data.get("notice"), "%d.%m.%Y %H:%M")
        if data.get("notice")
        else None
    )
    await update_task(
        session,
        task_id=int(data.get("task_id")),
        name=data.get("name"),
        desc=data.get("desc"),
        tag=data.get("tag"),
        _date=_date,
        _time=_time,
        notice=notice,
    )
    await callback.answer("☑️ Задача сохранена")
    await manager.done()


async def edit_name_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(name=text)
    bot: Bot = manager.middleware_data["bot"]
    await message.delete()
    await manager.switch_to(EditTasksSG.task_edit, show_mode=ShowMode.EDIT)


async def edit_desc_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(desc=text)
    bot: Bot = manager.middleware_data["bot"]
    await message.delete()
    await manager.switch_to(EditTasksSG.task_edit, show_mode=ShowMode.EDIT)


async def edit_tag(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
    *args,
) -> None:
    manager.dialog_data.update(tag=callback.data.split(":")[1])
    await manager.switch_to(EditTasksSG.task_edit)


async def edit_date(
    callback: CallbackQuery,
    widget: Calendar,
    manager: DialogManager,
    selected_date: date,
):
    manager.dialog_data["date"] = str(selected_date.strftime("%d.%m.%Y"))
    manager.dialog_data["notice"] = None
    await manager.switch_to(EditTasksSG.due_hour)


async def edit_hour(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    hour: str,
):
    manager.dialog_data["time"] = hour
    await manager.switch_to(EditTasksSG.due_minute)


async def save_due_edit(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    minute: str,
):
    manager.dialog_data["time"] = f"{manager.dialog_data['time']}:{minute}"
    await manager.switch_to(EditTasksSG.task_edit)


async def skip_hours(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
):
    manager.dialog_data["due"] = (
        manager.dialog_data["date"] + " " + manager.dialog_data["time"]
    )


async def edit_notice(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    notice: str,
):
    _date, _time = itemgetter("date", "time")(manager.dialog_data)
    notice: datetime = datetime.strptime(
        str(_date + " " + _time),
        "%d.%m.%Y %H:%M",
    ) - timedelta(minutes=int(notice))
    manager.dialog_data["notice"] = notice.strftime("%d.%m.%Y %H:%M")
    await manager.switch_to(EditTasksSG.task_edit)


async def delete_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    session: AsyncSession = manager.middleware_data.get("session")
    await callback.answer("❌ Задача удалена")
    await change_status_db(session, int(manager.dialog_data.get("task_id")))
    # names = await get_tasks_names(session, callback.from_user.id)
    # manager.dialog_data["task_names"] = [(i, str(j)) for i, j in names]
    # await manager.switch_to(ShowTasksSG.start)
    await manager.done()


async def complete_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    session: AsyncSession = manager.middleware_data.get("session")
    await callback.answer("✅ Задача выполнена")
    await change_status_db(session, int(manager.dialog_data.get("task_id")), status=2)
    await manager.done()
