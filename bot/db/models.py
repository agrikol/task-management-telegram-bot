from datetime import datetime
from bot.db.base import Base
from sqlalchemy import BigInteger, Integer, DateTime, Text, func, ForeignKey, Uuid, text
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

    task: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="delete"
    )


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=True)
    due: Mapped[str] = mapped_column(Text, nullable=True)
    tag: Mapped[str] = mapped_column(Text, nullable=True)
    notice: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )
    status: Mapped[Integer] = mapped_column(Integer, default=1, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="task")

    def __str__(self):
        return f"User_id: {self.user_id}, Name: {self.name}, Desc: {self.desc},\
        Due: {self.due}, Tag: {self.tag}, Notice: {self.notice}, Status: {self.status}"

    def to_dict(self):
        return {
            "name": self.name,
            "desc": self.desc,
            "due": self.due,
            "tag": self.tag,
            "notice": self.notice,
            "user_id": self.user_id,
        }
