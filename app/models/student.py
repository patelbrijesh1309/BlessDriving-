from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.student_language import StudentLanguage
    from app.models.student_enrollment import StudentEnrollment


class Student(Base):
    __tablename__ = "students"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    pickup_address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    emergency_contact: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="student",
    )

    languages: Mapped[list["StudentLanguage"]] = relationship(
    "StudentLanguage",
    back_populates="student",
    cascade="all, delete-orphan",
    )

    enrollments: Mapped[list["StudentEnrollment"]] = relationship(
    "StudentEnrollment",
    back_populates="student",
    cascade="all, delete-orphan",
    )