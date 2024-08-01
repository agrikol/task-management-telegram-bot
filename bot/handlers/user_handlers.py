from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router


router: Router = Router()


@router.message(Command("start"))
async def command_start_process(message: Message):
    await message.answer("You are in start handler")
