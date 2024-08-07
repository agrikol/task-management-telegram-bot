from aiogram.types import User
from aiogram_dialog import DialogManager


async def get_name(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    username = event_from_user.full_name or event_from_user.username
    return {"name": username}