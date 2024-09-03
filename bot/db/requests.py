from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import User
from sqlalchemy.dialects.postgresql import insert


async def add_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    username: str | None = None,
    last_name: str | None = None,
):

    stmt = insert(User).values(
        {
            User.telegram_id: telegram_id,
            User.first_name: first_name,
            User.username: username,
            User.last_name: last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=[User.telegram_id],
        set_={
            User.first_name: first_name,
            User.username: username,
            User.last_name: last_name,
        },
    )
    await session.execute(stmt)
    await session.commit()
