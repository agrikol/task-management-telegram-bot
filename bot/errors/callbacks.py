from aiogram.types import ErrorEvent


async def on_outdated_intent(event: ErrorEvent):
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "❗️ Сперва закройте другие активные окна ❗️"
        )
