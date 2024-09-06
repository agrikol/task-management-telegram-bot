from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from bot.states.states import CreateTaskSG
from aiogram.types import Message
from aiogram_dialog.widgets.input import TextInput


# def name_check(text: str) -> str:
#     if bool(text):
#         return text
#     raise ValueError


async def add_name_handler(
    message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
) -> None:
    dialog_manager.dialog_data.update(name=text)
    await dialog_manager.switch_to(CreateTaskSG.start)


async def add_desc_handler(
    message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
) -> None:
    dialog_manager.dialog_data.update(desc=text)
    await dialog_manager.switch_to(CreateTaskSG.start)


async def add_category(
    callback: CallbackQuery,
    widget: SwitchTo,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data.update(categ=callback.data)


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
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(CreateTaskSG.start)
