from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from bot.states.states import AdminSG
from aiogram_dialog.api.entities import ShowMode


admin_router: Router = Router()


@admin_router.message(Command("admin"))
async def process_admin_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await message.delete()
    await dialog_manager.start(
        AdminSG.start, mode=StartMode.NORMAL, show_mode=ShowMode.EDIT
    )
