import logging

from aiogram import Bot
from bot.service.delay_services.consumer import DelayedMessageConsumer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from nats.aio.client import Client
from nats.js.client import JetStreamContext

logger = logging.getLogger(__name__)


async def start_delayed_consumer(
    nc: Client,
    js: JetStreamContext,
    bot: Bot,
    session: async_sessionmaker,
    subject: str,
    stream: str,
    durable_name: str,
) -> None:
    consumer = DelayedMessageConsumer(
        nc=nc,
        js=js,
        bot=bot,
        session=session,
        subject=subject,
        stream=stream,
        durable_name=durable_name,
    )
    logger.info("Starting consumer")
    await consumer.start()
