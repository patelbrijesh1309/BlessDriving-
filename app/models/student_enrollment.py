from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.course import Course


class StudentEnrollment(Base):
    __tablename__ = "student_enrollments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )

    enrollment_date: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="enrollments",
    )

    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="enrollments",
    )