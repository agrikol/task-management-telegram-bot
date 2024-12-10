from nats.js.client import JetStreamContext
from datetime import datetime, timezone
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.requests import get_user_timezone


async def publish_delay(
    js: JetStreamContext,
    session: AsyncSession,
    user_id: int,
    subject: str,
    delay: datetime,
    task_id: int,
):
    utcnow = datetime.now(timezone.utc).replace(tzinfo=None)
    tz: str = await get_user_timezone(session, user_id) or "Europe/Moscow"
    tz_offset = pytz.timezone(tz).utcoffset(utcnow)
    delay: float = (delay - (utcnow + tz_offset)).total_seconds()
    headers = {
        "Tg-Delayed-Chat-ID": str(user_id),
        "Tg-Delayed-Msg-Timestamp": str(datetime.now().timestamp()),
        "Tg-Delayed-Msg-Delay": str(delay),
        "Tg-Delayed-Task-ID": str(task_id),
    }

    await js.publish(subject, headers=headers)
