from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.language import Language


class StudentLanguage(Base):
    __tablename__ = "student_languages"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    language_id: Mapped[int] = mapped_column(
        ForeignKey("languages.id", ondelete="CASCADE"),
        primary_key=True,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="languages",
    )

    language: Mapped["Language"] = relationship(
        "Language",
    )
