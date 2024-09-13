from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.db.models import User, Task
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


async def add_task(
    session: AsyncSession,
    user_id: int,
    name: str,
    desc: str | None = None,
    due: str | None = None,
    categ: str | None = None,
    notice: str | None = None,
):
    stmt = insert(Task).values(
        {
            Task.name: name,
            Task.desc: desc,
            Task.due: due,
            Task.categ: categ,
            Task.notice: notice,
            Task.user_id: user_id,
        }
    )
    stmt = stmt.on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()


async def get_task_info(session: AsyncSession, task_id: int):
    stmt = select(Task).where(Task.task_id == task_id)
    res = await session.execute(stmt)
    return res.scalar()


async def get_tasks_names(session: AsyncSession, user_id: int):
    stmt = select(Task.name, Task.task_id).where(Task.user_id == user_id)
    res = await session.execute(stmt)
    return res.fetchall()
