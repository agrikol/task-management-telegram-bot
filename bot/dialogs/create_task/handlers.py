from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from states.states import CreateTaskSG, ShowTaskSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import ManagedTextInput


def name_check(text: str) -> str:
    if bool(text):
        return text
    raise ValueError


async def correct_age_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:

    await message.answer(text=f"{text}")
    await dialog_manager.switch_to(CreateTaskSG.start)


async def error_age_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(
        text="Вы ввели некорректное имя задачи. Попробуйте еще раз",
    )
