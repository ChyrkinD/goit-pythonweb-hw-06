from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )

    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped["Grade"] = relationship("Grade", back_populates="subject")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name}, teacher_id={self.teacher_id})>"
