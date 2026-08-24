from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CourseModule(Base):
    __tablename__ = "course_modules"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    order_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    course = relationship(
        "Course",
        back_populates="modules",
    )