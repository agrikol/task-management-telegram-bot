from datetime import datetime
from bot.db.base import Base
from sqlalchemy import BigInteger, DateTime, Text, func, ForeignKey, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=True)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)

    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="delete"
    )


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"

    task_id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=True)
    due: Mapped[str] = mapped_column(Text, nullable=True)
    categ: Mapped[str] = mapped_column(Text, nullable=True)
    notice: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )

    user: Mapped["User"] = relationship("User", back_populates="tasks")
