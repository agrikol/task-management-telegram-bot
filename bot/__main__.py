import asyncio, logging
from aiogram import Bot, Dispatcher
from handlers import commands
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config_reader import config
from dialogs.start.dialogs import start_dialog
from aiogram_dialog import setup_dialogs


async def main():
    logging.basicConfig(level=logging.INFO)
    bot: Bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp: Dispatcher = Dispatcher()
    dp.include_router(commands.commands_router)
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot, allowed_updates=[]))


if __name__ == "__main__":
    asyncio.run(main())
