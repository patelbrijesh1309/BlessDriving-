from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InstructorLanguage(Base):
    __tablename__ = "instructor_languages"

    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("instructors.user_id", ondelete="CASCADE"),
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

    instructor = relationship(
        "Instructor",
        back_populates="languages",
    )

    language = relationship("Language")