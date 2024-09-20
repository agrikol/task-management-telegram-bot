from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.db.models import User, Task
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, and_
from datetime import date, time, datetime


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
    _date: date | None = None,
    _time: time | None = None,
    tag: str | None = None,
    notice: datetime | None = None,
):
    stmt = insert(Task).values(
        {
            Task.name: name,
            Task.desc: desc,
            Task.date: _date,
            Task.time: _time,
            Task.tag: tag,
            Task.notice: notice,
            Task.user_id: user_id,
        }
    )
    stmt = stmt.on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()


async def update_task(
    session: AsyncSession,
    task_id: int,
    name: str,
    desc: str,
    _date: str,
    _time: str,
    tag: str,
    notice: datetime | None = None,
    status: int = 1,
):
    stmt = (
        update(Task)
        .where(Task.task_id == task_id)
        .values(
            {
                Task.name: name,
                Task.desc: desc,
                Task.date: _date,
                Task.time: _time,
                Task.tag: tag,
                Task.notice: notice,
                Task.status: status,
            }
        )
    )
    await session.execute(stmt)
    await session.commit()


async def change_status_db(session: AsyncSession, task_id: int, status: int = 0):
    stmt = update(Task).where(Task.task_id == task_id).values(status=status)
    await session.execute(stmt)
    await session.commit()


async def get_task_info(session: AsyncSession, task_id: int):
    stmt = select(Task).where(Task.task_id == task_id)
    res = await session.execute(stmt)
    return res.scalar()


async def get_tasks_names(session: AsyncSession, user_id: int, today: bool = False):
    stmt = select(Task.name, Task.tag, Task.date, Task.task_id).where(
        and_(Task.user_id == user_id, Task.status == 1)
    )
    if today:
        stmt = stmt.where(Task.date == date.today())
    res = await session.execute(stmt)
    return res.fetchall()


async def check_tasks_exist(session: AsyncSession, user_id: int):
    stmt = select(Task).where(and_(Task.user_id == user_id, Task.status == 1))
    res = await session.execute(stmt)
    tasks_exist = res.scalars().all()
    today_exists = any(date.today() == task.date for task in tasks_exist)
    return bool(tasks_exist), today_exists
