from typing import Callable, Awaitable, Any, Dict, cast
from aiogram.types import TelegramObject, Message
from aiogram import BaseMiddleware


class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[int]) -> None:
        super().__init__()
        self.admin_id = admin_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event = cast(Message, event)
        if event.from_user.id in self.admin_id:
            return await handler(event, data)
