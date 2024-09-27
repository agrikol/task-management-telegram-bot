from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def exit_admin(callback: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.done()
