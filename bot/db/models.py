from datetime import datetime
from bot.db import Base
from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    Date,
    Time,
    Text,
    func,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from datetime import date, time


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
    timezone: Mapped[str] = mapped_column(Text, nullable=True)

    task: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="delete"
    )


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    time: Mapped[Time] = mapped_column(Time, nullable=True)
    tag: Mapped[str] = mapped_column(Text, nullable=False)
    notice: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="task")

    def __str__(self):
        return f"User_id: {self.user_id}, Name: {self.name}, Desc: {self.desc},\
        Date: {self.date}, Time: {self.time}, Tag: {self.tag}, Notice: {self.notice},\
        Status: {self.status}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "desc": self.desc,
            "date": self.date,
            "time": self.time,
            "tag": self.tag,
            "notice": self.notice,
            "user_id": self.user_id,
        }
