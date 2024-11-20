import logging
from contextlib import suppress
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext
from bot.kb.kb import notice_kb


logger = logging.getLogger(__name__)


class DelayedMessageConsumer:
    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
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
        logger.info("!!!!!!!!!!INFO!!!!!!!!!!")
        logger.info(
            f"{sent_time + timedelta(seconds=delay)} {datetime.now().astimezone()}"
        )
        logger.info("!!!!!!!!!!INFO!!!!!!!!!!")

        if sent_time + timedelta(seconds=delay) > datetime.now().astimezone():
            new_delay = (
                sent_time + timedelta(seconds=delay) - datetime.now().astimezone()
            ).total_seconds()
            await msg.nak(delay=new_delay)
        else:
            chat_id = int(msg.headers.get("Tg-Delayed-Chat-ID"))
            with suppress(TelegramBadRequest):
                await self.bot.send_message(
                    chat_id=chat_id,
                    text="Отложенное сообщение",
                    reply_markup=notice_kb(),
                )
            await msg.ack()
            logger.info("Message deleted.")

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info("Consumer unsubscribed")
