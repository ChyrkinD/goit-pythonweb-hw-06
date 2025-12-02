from src.models.base import Base
from src.models.grade import Grade
from src.models.group import Group
from src.models.student import Student
from src.models.subject import Subject
from src.models.teacher import Teacher

__all__ = ["Base", "Grade", "Group", "Student", "Subject", "Teacher"]

print("Im using __init__.py to define models:", __all__)
