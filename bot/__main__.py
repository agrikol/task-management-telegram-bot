import asyncio, logging
from aiogram import Bot, Dispatcher
from handlers import user_handlers
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config_reader import config


async def main():
    logging.basicConfig(level=logging.INFO)
    bot: Bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp: Dispatcher = Dispatcher()
    dp.include_router(user_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=[])


if __name__ == "__main__":
    asyncio.run(main())
