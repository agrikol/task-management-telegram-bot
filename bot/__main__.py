import asyncio, logging
from aiogram import Bot, Dispatcher
from bot.handlers import commands
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config.config_reader import config
from bot.dialogs.start.dialogs import start_dialog
from bot.dialogs.create_task.dialogs import create_task_dialog
from bot.dialogs.get_tasks.dialogs import task_list_dialog
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.base import DefaultKeyBuilder
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from bot.db.base import Base
from bot.middlewares.session import CacheMiddleware, DbSessionMiddleware


async def main():

    logging.basicConfig(level=logging.INFO)

    engine = create_async_engine(url=str(config.db_dsn), echo=config.is_echo)

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)  # TODO: remove
        await connection.run_sync(Base.metadata.create_all)

    storage = RedisStorage(
        redis=Redis.from_url(str(config.redis_dsn)),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    dp: Dispatcher = Dispatcher(storage=storage)
    setup_dialogs(dp)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.message.outer_middleware(CacheMiddleware())
    dp.include_routers(
        commands.commands_router, start_dialog, create_task_dialog, task_list_dialog
    )

    bot: Bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot, allowed_updates=[]))


if __name__ == "__main__":
    asyncio.run(main())
