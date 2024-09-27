from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from bot.states.states import StartSG, AdminSG


admin_router: Router = Router()


@admin_router.message(Command("admin"))
async def process_admin_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(AdminSG.start, mode=StartMode.NORMAL)
