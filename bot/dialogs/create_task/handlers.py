from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select
from bot.states.states import CreateTaskSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime, timedelta

# def name_check(text: str) -> str:
#     if bool(text):
#         return text
#     raise ValueError


async def add_name_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(name=text)
    await manager.switch_to(CreateTaskSG.start)


async def add_desc_handler(
    message: Message, widget: TextInput, manager: DialogManager, text: str
) -> None:
    manager.dialog_data.update(desc=text)
    await manager.switch_to(CreateTaskSG.start)


async def add_category(
    callback: CallbackQuery,
    widget: SwitchTo,
    manager: DialogManager,
) -> None:
    manager.dialog_data.update(categ=callback.data)


# async def error_age_handler(
#     message: Message,
#     widget: ManagedTextInput,
#     dialog_manager: DialogManager,
#     error: ValueError,
# ):
#     await message.answer(
#         text="Вы ввели некорректное имя задачи. Попробуйте еще раз",
#     )


async def start_create_task(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(CreateTaskSG.start)


async def select_date(
    callback: CallbackQuery,
    widget: Calendar,
    manager: DialogManager,
    selected_date: date,
):
    manager.dialog_data["due"] = str(selected_date.strftime("%d.%m.%Y"))
    await manager.switch_to(CreateTaskSG.due_hour)


async def select_hour(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    hour: str,
):
    manager.dialog_data["time"] = hour
    print(manager.dialog_data)
    await manager.switch_to(CreateTaskSG.due_minute)


async def save_due(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    minute: str,
):
    manager.dialog_data["time"] = manager.dialog_data["time"] + ":" + minute
    await manager.switch_to(CreateTaskSG.start)


async def save_notice(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    notice: str,
):
    _date = manager.dialog_data.get("due") or str(
        (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    )
    _time = manager.dialog_data.get("time") or "12:00"
    notice: datetime = datetime.strptime(
        str(_date + " " + _time),
        "%d.%m.%Y %H:%M",
    ) - timedelta(minutes=int(notice))
    manager.dialog_data["notice"] = str(notice.strftime("%d.%m.%Y %H:%M"))
    await manager.switch_to(CreateTaskSG.start)
