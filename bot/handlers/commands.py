from aiogram import Router, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.filters import CommandStart, Command
from aiogram_dialog import DialogManager, StartMode
from bot.states.states import StartSG, FeedbackSG
from bot.db.requests import add_user, add_user_timezone
from sqlalchemy.ext.asyncio import AsyncSession
from timezonefinder import TimezoneFinder

commands_router: Router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    session: AsyncSession,
) -> None:
    await add_user(
        session,
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.from_user.last_name,
    )
    await dialog_manager.start(StartSG.start, mode=StartMode.RESET_STACK)


@commands_router.message(Command("feedback"))
async def process_feedback_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await message.delete()
    await dialog_manager.start(FeedbackSG.start, mode=StartMode.NORMAL)


@commands_router.message(Command("timezone"))
async def process_location_command(message: Message) -> None:
    location_btn = KeyboardButton(text="Share current location", request_location=True)
    cancel_btn = KeyboardButton(text="Cancel")
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[location_btn], [cancel_btn]], resize_keyboard=True
    )
    await message.answer(
        "Please, share your location:",
        reply_markup=keyboard,
    )


@commands_router.message(F.location)
async def process_location(message: Message, session: AsyncSession) -> None:
    # TODO: Refactor this
    await message.delete()
    tf = TimezoneFinder()
    timezone = tf.timezone_at(
        lng=message.location.longitude, lat=message.location.latitude
    )
    await add_user_timezone(session, message.from_user.id, timezone)
    await message.answer(
        f"Timezone: {timezone}",
        reply_markup=ReplyKeyboardRemove(),
    )


@commands_router.message(F.text == "Cancel")
async def process_cancel(message: Message, dialog_manager: DialogManager) -> None:
    # TODO: Refactor this
    await message.delete()
    await message.answer("Thanks for using me!", reply_markup=ReplyKeyboardRemove())
    await dialog_manager.start(StartSG.start, mode=StartMode.RESET_STACK)
