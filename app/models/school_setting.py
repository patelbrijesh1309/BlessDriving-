from datetime import datetime, time


from sqlalchemy import DateTime, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SchoolSetting(Base):
    __tablename__ = "school_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        default=1,
    )

    school_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    opening_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    closing_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    default_lesson_duration: Mapped[int] = mapped_column(
        Integer,
        default=60,
    )

    buffer_minutes: Mapped[int] = mapped_column(
        Integer,
        default=15,
    )

    cancellation_hours: Mapped[int] = mapped_column(
        Integer,
        default=24,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default="Australia/Sydney",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

