import random
from datetime import datetime, timedelta

from faker import Faker
from logger import logger

from connection import session
from models import (
    Grade,
    Group,
    Student,
    Subject,
    Teacher
)

fake = Faker("en_US")

if __name__ == "__main__":
    try:
        # Groups
        groups = [Group(name=f"Group №{i}") for i in range(1, 4)]
        session.add_all(groups)
        session.commit()
        logger.info(f"Groups added in session: {groups}")

        # Teachers
        teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
        session.add_all(teachers)
        session.commit()
        logger.info(f"Teachers added in session: {teachers}")

        # Subjects
        teacher_ids = [t.id for t in teachers]
        mock_data_for_subjects = subjects_data_en = [
            ("English Language", teacher_ids[3]),
            ("Fundamentals of Programming", teacher_ids[1]),
            ("Mathematical Analysis", teacher_ids[0]),
            ("Algorithms and Data Structures", teacher_ids[2]),
            ("Physics", teacher_ids[0]),
            ("Computer Networks", teacher_ids[3]),
            ("Databases", teacher_ids[1]),
            ("System Analysis", teacher_ids[4]),
        ]
        subjects = [Subject(name=name, teacher_id=teacher_id) for name, teacher_id in mock_data_for_subjects]
        session.add_all(subjects)
        session.commit()
        logger.info(f"Subjects added in session: {subjects}")

        # Students
        students = [Student(
            name=fake.name(),
            group_id=random.choice([group.id for group in groups]),
        ) for _ in range(50)]
        session.add_all(students)
        session.commit()
        logger.info(f"Students added in session: {students[:5]}...")

        # Grades
        student_ids = [s.id for s in students]
        subject_ids = [s.id for s in subjects]
        grades = []
        start_date = datetime(2024, 9, 1)
        end_date = datetime(2025, 1, 15)

        for student_id in student_ids:
            student_subjects = random.sample(
                subject_ids, k=random.randint(4, len(subject_ids))
            )

            for subject_id in student_subjects:
                num_grades = random.randint(5, 20)
                for _ in range(num_grades):
                    random_date = start_date + timedelta(
                        days=random.randint(0, (end_date - start_date).days)
                    )

                    grade_value = random.randint(60, 100)

                    grades.append(
                        Grade(
                            student_id=student_id,
                            subject_id=subject_id,
                            grade=grade_value,
                            grade_date=random_date.date(),
                        )
                    )
        session.add_all(grades)
        logger.info(f"Grades added in session: {grades[:5]}...")
        session.commit()
        logger.info("Transaction committed.")
    except Exception as e:
        session.rollback()
        logger.error(f"Transaction failed, rolled back. Error: {e}")
    finally:
        session.close()