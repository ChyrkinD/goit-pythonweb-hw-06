from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )

    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped["Grade"] = relationship("Grade", back_populates="student")

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, name={self.name}, group_id={self.group_id})>"
