from aiogram import Bot
from operator import itemgetter
from datetime import datetime, date
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select
from bot.states.states import CreateTaskSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.requests import add_task
from bot.service.delay_services.publisher import publish_delay
from aiogram_dialog.api.entities import ShowMode


async def add_name_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    bot: Bot = manager.middleware_data["bot"]
    manager.dialog_data.update(name=text)
    await message.delete()
    await manager.switch_to(CreateTaskSG.start, show_mode=ShowMode.EDIT)


async def add_desc_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(desc=text)
    bot: Bot = manager.middleware_data["bot"]
    await message.delete()
    await manager.switch_to(CreateTaskSG.start, show_mode=ShowMode.EDIT)


async def add_tag(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
    *args,
) -> None:
    manager.dialog_data.update(tag=callback.data.split(":")[1])
    await manager.switch_to(CreateTaskSG.start)


# async def error_age_handler(
#     message: Message,
#     widget: ManagedTextInput,
#     dialog_manager: DialogManager,
#     error: ValueError,
# ):
#     await message.answer(
#         text="Вы ввели некорректное имя задачи. Попробуйте еще раз",
#     )


async def select_date(
    callback: CallbackQuery,
    widget: Calendar,
    manager: DialogManager,
    selected_date: date,
):
    manager.dialog_data["date"] = str(selected_date.strftime("%d.%m.%Y"))
    manager.dialog_data["notice"] = None
    await manager.switch_to(CreateTaskSG.due_hour)


async def select_hour(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    hour: str,
):
    manager.dialog_data["time"] = hour
    await manager.switch_to(CreateTaskSG.due_minute)


async def save_due(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    minute: str,
):
    manager.dialog_data["time"] = f"{manager.dialog_data['time']}:{minute}"
    await manager.switch_to(CreateTaskSG.start)


async def save_notice(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    notice: str,
):
    _date = manager.dialog_data.get("date")
    _time = manager.dialog_data.get("time")
    notice: datetime = datetime.strptime(
        str(_date + " " + _time),
        "%d.%m.%Y %H:%M",
    ) - timedelta(minutes=int(notice))
    manager.dialog_data["notice"] = notice.strftime("%d.%m.%Y %H:%M")
    await manager.switch_to(CreateTaskSG.start)


async def save_task(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    data: dict = manager.dialog_data
    session: AsyncSession = manager.middleware_data.get("session")
    _date: date = datetime.strptime(data.get("date"), "%d.%m.%Y").date()
    _time = (
        datetime.strptime(data.get("time"), "%H:%M").time()
        if data.get("time")
        else None
    )
    notice: datetime | None = (
        datetime.strptime(data.get("notice"), "%d.%m.%Y %H:%M")
        if data.get("notice")
        else None
    )

    task_id = await add_task(
        session,
        user_id=callback.from_user.id,
        name=data.get("name"),
        desc=data.get("desc"),
        tag=data.get("tag", "0"),
        _date=_date,
        _time=_time,
        notice=notice,
    )
    await callback.answer("☑️ Задача сохранена")

    if notice:
        js, subject = itemgetter("js", "subject")(manager.middleware_data)
        await publish_delay(
            js=js,
            session=session,
            user_id=callback.from_user.id,
            task_id=task_id,
            subject=subject,
            delay=notice,
        )
    await manager.done()


async def clear_hours(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
):
    manager.dialog_data["time"] = ""
