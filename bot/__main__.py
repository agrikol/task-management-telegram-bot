import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis
from bot.db.base import Base
from bot.handlers.commands import commands_router
from bot.handlers.admin_command import admin_router
from bot.config.config_reader import Settings
from bot.dialogs.start.dialogs import start_dialog
from bot.dialogs.admin.dialogs import admin_dialog
from bot.dialogs.create_task.dialogs import create_task_dialog
from bot.dialogs.get_tasks.dialogs import task_list_dialog
from bot.dialogs.feedback.dialogs import feedback_dialog
from bot.middlewares.session import CacheMiddleware, DbSessionMiddleware
from bot.middlewares.middlewares import AdminCheckerMiddleware


async def main():
    logging.basicConfig(level=logging.INFO)
    config = Settings()

    engine = create_async_engine(url=str(config.db_dsn), echo=config.is_echo)
    admin_ids = config.admin_id

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    async with engine.begin() as connection:
        # await connection.run_sync(Base.metadata.drop_all)  # TODO: remove
        await connection.run_sync(Base.metadata.create_all)

    storage = RedisStorage(
        redis=Redis.from_url(str(config.redis_dsn)),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    dp: Dispatcher = Dispatcher(storage=storage)
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.message.outer_middleware(CacheMiddleware())
    admin_router.message.outer_middleware(AdminCheckerMiddleware(admin_ids=admin_ids))
    dp.workflow_data.update({"admin_ids": admin_ids})

    setup_dialogs(dp)

    dp.include_routers(
        commands_router,
        admin_router,
        start_dialog,
        admin_dialog,
        create_task_dialog,
        task_list_dialog,
        feedback_dialog,
    )
    bot: Bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot, allowed_updates=[]))


if __name__ == "__main__":
    asyncio.run(main())
