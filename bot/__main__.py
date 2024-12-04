import json
import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.client.default import DefaultBotProperties
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis
from bot.db.base import Base
from bot.config.config_reader import Settings
from bot.handlers.commands import commands_router
from bot.handlers.admin_command import admin_router
from bot.handlers.name_handler import task_name_router
from bot.dialogs import dialogs
from bot.middlewares.session import CacheMiddleware, DbSessionMiddleware
from bot.middlewares.admin_checker import AdminCheckerMiddleware
from bot.utils.connect_nats import connect_nats
from bot.utils.start_stream import create_stream
from bot.utils.start_consumer import start_delayed_consumer
from bot.utils.json_serializer import JsonSerializer
from bot.errors.callbacks import on_outdated_intent, on_unknown_intent
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    config = Settings()
    admin_ids = config.admin_id

    engine = create_async_engine(url=str(config.db_dsn), echo=config.is_echo)
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    async with engine.begin() as connection:
        # await connection.run_sync(Base.metadata.drop_all)  # TODO: remove
        await connection.run_sync(Base.metadata.create_all)

    storage = RedisStorage(
        redis=Redis.from_url(str(config.redis_dsn)),
        key_builder=DefaultKeyBuilder(with_destiny=True),
        json_dumps=lambda obj: json.dumps(obj, default=JsonSerializer.default),
    )

    dp: Dispatcher = Dispatcher(storage=storage)
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.message.outer_middleware(CacheMiddleware())
    admin_router.message.outer_middleware(AdminCheckerMiddleware(admin_ids=admin_ids))
    dp.workflow_data.update({"admin_ids": admin_ids})

    nc, js = await connect_nats(servers=config.nats_servers)
    stream = await create_stream(
        js=js,
        stream_name=config.nats_delayed_consumer_stream,
        subjects=[config.nats_delayed_consumer_subject],
    )
    logger.info(stream)

    setup_dialogs(dp)
    dp.include_routers(commands_router, admin_router, task_name_router, *dialogs)
    dp.errors.register(on_outdated_intent, ExceptionTypeFilter(OutdatedIntent))
    dp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    bot: Bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await asyncio.gather(
            dp.start_polling(bot, js=js, subject=config.nats_delayed_consumer_subject),
            start_delayed_consumer(
                nc=nc,
                js=js,
                bot=bot,
                session=Sessionmaker,
                subject=config.nats_delayed_consumer_subject,
                stream=config.nats_delayed_consumer_stream,
                durable_name=config.nats_delayed_consumer_durable_name,
            ),
        )
    except Exception as e:
        logger.error(e)
    finally:
        await nc.close()
        await engine.dispose()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
