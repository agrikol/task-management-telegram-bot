from typing import Callable, Awaitable, Any, Dict, cast
from aiogram.types import TelegramObject, Message
from aiogram import BaseMiddleware


class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[str]) -> None:
        super().__init__()
        self.admin_ids = admin_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event = cast(Message, event)
        print("!!!!!!!")
        print(
            event.from_user.id,
            self.admin_ids,
            type(event.from_user.id),
            type(self.admin_ids),
        )
        if str(event.from_user.id) not in self.admin_ids:
            return
        return await handler(event, data)
