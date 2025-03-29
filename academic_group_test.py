import pytest
from datetime import datetime
from faker import Faker
from AcademicGroup import AcademicGroup, Student


def generate_students(count: int) -> list[Student]:
    fake = Faker()
    students = []

    for i in range(count - 1):
        student = Student(
            id=i + 1,
            full_name=fake.name(),
            date_of_receipt=datetime.fromordinal(fake.date_between(start_date='-4y', end_date='today').toordinal())
        )
        students.append(student)
    students.append(Student(
        id= len(students) + 1,
        full_name = "Oleg Gerbylev",
        date_of_receipt = datetime(2023, 9, 1)
    ))
    return students


def test_add_student():
    students = generate_students(8)
    academic_group1 = AcademicGroup(5, 10)
    for student in students:
        academic_group1.add_student(student)
    assert len(academic_group1) == 8


def test_delete_student():
    students = generate_students(8)
    academic_group1 = AcademicGroup(5, 10)
    for student in students:
        academic_group1.add_student(student)

    academic_group1.delete_student(4)
    assert len(academic_group1) == 7

def test_full_student():
    students = generate_students(8)
    academic_group1 = AcademicGroup(5, 7)
    with pytest.raises(Exception, match="Нельзя добавить, достигнут максимум по студентам"):
        for student in students:
            academic_group1.add_student(student)

def test_search():
    students = generate_students(8)
    academic_group1 = AcademicGroup(5, 10)
    for student in students:
        academic_group1.add_student(student)
    students = academic_group1.search("Oleg")
    assert students[-1].full_name == "Oleg Gerbylev"

if __name__ == "__main__":
    pytest.main()
