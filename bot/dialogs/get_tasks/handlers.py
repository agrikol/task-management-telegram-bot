from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select
from bot.states.states import ShowTasksSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.requests import (
    update_task,
    get_task_info,
    change_status_db,
    get_tasks_names,
)
from bot.db.models import Task


async def listing_tasks(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    *args,
    **kwargs,
):
    session: AsyncSession = manager.middleware_data.get("session")
    task_id = callback.data.split(":")[1]
    task: Task = await get_task_info(session, int(task_id))
    manager.dialog_data.update(task.to_dict())
    manager.dialog_data.update(task_id=task_id)
    await manager.switch_to(ShowTasksSG.task_edit)


async def edit_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    data: dict = manager.dialog_data
    session: AsyncSession = manager.middleware_data.get("session")
    print(data)
    await update_task(
        session,
        task_id=int(data.get("task_id")),
        name=data.get("name"),
        desc=data.get("desc"),
        tag=data.get("tag"),
        due=data.get("due"),
        notice=data.get("notice"),
    )
    await callback.answer("☑️ Задача сохранена")
    names = await get_tasks_names(session, callback.from_user.id)
    manager.dialog_data["task_names"] = [(i, str(j)) for i, j in names]
    await manager.switch_to(ShowTasksSG.start)


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


async def edit_tag(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
    *args,
) -> None:
    manager.dialog_data.update(tag=callback.data.split(":")[1])
    print(manager.dialog_data)
    await manager.switch_to(ShowTasksSG.task_edit)


async def edit_date(
    callback: CallbackQuery,
    widget: Calendar,
    manager: DialogManager,
    selected_date: date,
):
    manager.dialog_data["temp_due"] = str(selected_date.strftime("%d.%m.%Y"))
    await manager.switch_to(ShowTasksSG.due_hour)


async def edit_hour(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    hour: str,
):
    manager.dialog_data["time"] = hour
    await manager.switch_to(ShowTasksSG.due_minute)


async def save_due_edit(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    minute: str,
):
    manager.dialog_data["due"] = (
        manager.dialog_data["temp_due"]
        + " "
        + manager.dialog_data["time"]
        + ":"
        + minute
    )
    await manager.switch_to(ShowTasksSG.task_edit)  # TODO fix notice


async def skip_hours(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
):
    manager.dialog_data["due"] = (
        manager.dialog_data["temp_due"] + " " + manager.dialog_data["due"].split(" ")[1]
    )  # TODO: fix this


async def edit_notice(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    notice: str,
):
    _date, _time = manager.dialog_data.get("due").split(" ")
    notice: datetime = datetime.strptime(
        str(_date + " " + _time),
        "%d.%m.%Y %H:%M",
    ) - timedelta(minutes=int(notice))
    manager.dialog_data["notice"] = notice.strftime("%d.%m.%Y %H:%M")
    await manager.switch_to(ShowTasksSG.task_edit)


async def delete_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    session: AsyncSession = manager.middleware_data.get("session")
    await callback.answer("❌ Задача удалена")
    await change_status_db(session, int(manager.dialog_data.get("task_id")))
    names = await get_tasks_names(session, callback.from_user.id)
    manager.dialog_data["task_names"] = [(i, str(j)) for i, j in names]
    await manager.switch_to(ShowTasksSG.start)


async def complete_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    session: AsyncSession = manager.middleware_data.get("session")
    await callback.answer("✅ Задача выполнена")
    await change_status_db(session, int(manager.dialog_data.get("task_id")), status=2)
    names = await get_tasks_names(session, callback.from_user.id)
    manager.dialog_data["task_names"] = [(i, str(j)) for i, j in names]
    await manager.switch_to(ShowTasksSG.start)
