from aiogram import F
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode
from bot.states.states import StartSG


commands_router: Router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(StartSG.start, mode=StartMode.RESET_STACK)
