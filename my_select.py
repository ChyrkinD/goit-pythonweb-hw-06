from sqlalchemy import select, func, desc

from src.connection import session
from src.models import Student, Group, Teacher, Subject, Grade


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    stmt = (
        select(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id, Student.name)
        .order_by(desc("avg_grade"))
        .limit(5)
    )

    result = session.execute(stmt).all()
    print("\n## 1. 5 студентів із найбільшим середнім балом:")
    for name, avg_grade in result:
        print(f"Студент: {name}, Середній бал: {avg_grade}")

# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id: int = 1):
    stmt = (
        select(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id, Student.name)
        .order_by(desc("avg_grade"))
        .limit(1)
    )

    result = session.execute(stmt).first()

    subject_name = session.execute(select(Subject.name).where(Subject.id == subject_id)).scalar_one_or_none()

    print(f"\n## 2. Студент із найвищим середнім балом з '{subject_name}':")
    if result:
        name, avg_grade = result
        print(f"Студент: {name}, Середній бал: {avg_grade}")

# Знайти середній бал у групах з певного предмета.
def select_3(subject_id: int = 2):
    stmt = (
        select(
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Group)  # Починаємо з Group, щоб було явно
        .join(Student)
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.name)
    )

    result = session.execute(stmt).all()
    subject_name = session.execute(select(Subject.name).where(Subject.id == subject_id)).scalar_one_or_none()

    print(f"\n## 3. Середній бал у групах з '{subject_name}':")
    for group_name, avg_grade in result:
        print(f"Група: {group_name}, Середній бал: {avg_grade}")

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    stmt = select(func.round(func.avg(Grade.grade), 2))

    avg_grade_total = session.execute(stmt).scalar_one()

    print("\n## 4. Середній бал на потоці (за всіма оцінками):")
    print(f"Середній бал: {avg_grade_total}")

# Знайти які курси читає певний викладач.
def select_5(teacher_id: int = 1):
    stmt = (
        select(Subject.name)
        .join(Teacher)
        .where(Teacher.id == teacher_id)
    )

    result = session.execute(stmt).scalars().all()
    teacher_name = session.execute(select(Teacher.fullname).where(Teacher.id == teacher_id)).scalar_one_or_none()

    print(f"\n## 5. Курси, які читає викладач {teacher_name}:")
    for subject_name in result:
        print(f"- {subject_name}")

# Знайти список студентів у певній групі.
def select_6(group_id: int = 3):
    stmt = (
        select(Student.name)
        .where(Student.group_id == group_id)
        .order_by(Student.name)
    )

    result = session.execute(stmt).scalars().all()
    group_name = session.execute(select(Group.name).where(Group.id == group_id)).scalar_one_or_none()

    print(f"\n## 6. Студенти у групі '{group_name}':")
    for student_name in result:
        print(f"- {student_name}")

# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id: int = 1, subject_id: int = 3):
    stmt = (
        select(
            Student.name,
            Grade.grade
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .where(Group.id == group_id)
        .where(Grade.subject_id == subject_id)
        .order_by(Student.name, Grade.grade_date)
    )

    result = session.execute(stmt).all()
    group_name = session.execute(select(Group.name).where(Group.id == group_id)).scalar_one_or_none()
    subject_name = session.execute(select(Subject.name).where(Subject.id == subject_id)).scalar_one_or_none()

    print(f"\n## 7. Оцінки студентів групи '{group_name}' з '{subject_name}':")
    for student_name, grade in result:
        print(f"- {student_name}: {grade}")

# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id: int = 4):
    stmt = (
        select(
            func.round(func.avg(Grade.grade), 2)
        )
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .where(Teacher.id == teacher_id)
    )

    avg_grade = session.execute(stmt).scalar_one_or_none()
    teacher_name = session.execute(select(Teacher.fullname).where(Teacher.id == teacher_id)).scalar_one_or_none()

    print(f"\n## 8. Середній бал, який ставить викладач {teacher_name}:")
    print(f"Середній бал: {avg_grade}")

# Знайти список курсів, які відвідує певний студент.
def select_9(student_id: int = 10):
    stmt = (
        select(Subject.name)
        .select_from(Student)
        .join(Grade)
        .join(Subject)
        .where(Student.id == student_id)
        .distinct()
    )

    result = session.execute(stmt).scalars().all()
    student_name = session.execute(select(Student.name).where(Student.id == student_id)).scalar_one_or_none()

    print(f"\n## 9. Курси, які відвідує студент {student_name}:")
    for subject_name in result:
        print(f"- {subject_name}")

# Список курсів, які певному студенту читає певний викладач.
def select_10(student_id: int = 5, teacher_id: int = 1):
    stmt = (
        select(Subject.name)
        .select_from(Student)
        .join(Grade)
        .join(Subject)
        .join(Teacher)
        .where(Student.id == student_id)
        .where(Teacher.id == teacher_id)
        .distinct()
    )

    result = session.execute(stmt).scalars().all()
    student_name = session.execute(select(Student.name).where(Student.id == student_id)).scalar_one_or_none()
    teacher_name = session.execute(select(Teacher.fullname).where(Teacher.id == teacher_id)).scalar_one_or_none()

    print(f"\n## 10. Курси, які студент {student_name} відвідує у викладача {teacher_name}:")
    if result:
        for subject_name in result:
            print(f"- {subject_name}")
    else:
        print("Не знайдено спільних курсів.")


if __name__ == "__main__":
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()