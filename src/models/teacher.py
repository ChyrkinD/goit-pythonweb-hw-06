from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)

    subjects: Mapped["Subject"] = relationship("Subject", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher(id={self.id}, fullname={self.fullname})>"
