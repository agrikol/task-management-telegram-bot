import logging
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from bot.db.requests import get_task_status
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext
from bot.utils.send_notice import send_notice
from sqlalchemy.ext.asyncio import async_sessionmaker


logger = logging.getLogger(__name__)


class DelayedMessageConsumer:
    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        session: async_sessionmaker,
        subject: str,
        stream: str,
        durable_name: str,
    ) -> None:
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name
        self.session = session

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True,
        )

    async def on_message(self, msg: Msg) -> None:
        sent_time: datetime = datetime.fromtimestamp(
            float(msg.headers.get("Tg-Delayed-Msg-Timestamp")), tz=timezone.utc
        )
        delay: float = float(msg.headers.get("Tg-Delayed-Msg-Delay"))
        if sent_time + timedelta(seconds=delay) > datetime.now().astimezone():
            new_delay = (
                sent_time + timedelta(seconds=delay) - datetime.now().astimezone()
            ).total_seconds()
            await msg.nak(delay=new_delay)
        else:
            # await self.js.delete_msg(
            #     stream_name=self.stream, seq=msg.metadata.sequence.stream
            # ) # TODO: probably msg should be deleted from stream when task status changed
            async with self.session() as session:
                status: int = await get_task_status(
                    session=session, task_id=int(msg.headers.get("Tg-Delayed-Task-ID"))
                )
            if status in (0, 2):
                await msg.ack()
                return
            chat_id = int(msg.headers.get("Tg-Delayed-Chat-ID"))
            task_id = msg.headers.get("Tg-Delayed-Task-ID")
            with suppress(TelegramBadRequest):
                await send_notice(
                    bot=self.bot, session=self.session, chat_id=chat_id, task_id=task_id
                )
            await msg.ack()
            logger.info("Message delivered.")

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info("Consumer unsubscribed")
