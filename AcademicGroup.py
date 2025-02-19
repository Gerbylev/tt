from dataclasses import dataclass
from datetime import datetime


@dataclass
class Student:
    id: int
    full_name: str
    date_of_receipt: datetime

    def __repr__(self) -> str:
        return f"""
Student id: {self.id}
Student fullname: {self.full_name}
Student date of receipt: {self.date_of_receipt}
"""

class AcademicGroup:

    def __init__(self, min_student: int, max_student: int):
        self.min_student = min_student
        self.max_student = max_student
        self.students: list[Student] = []

    def add_student(self, student: Student):
        if len(self.students) < self.max_student:
            self.students.append(student)
        else:
            raise Exception("Нельзя добавить, достигнут максимум по студентам")

    def delete_student(self, student_id: int) -> Student:
        if self.min_student >= len(self):
            raise Exception("Нельзя удалить, достигнут минимум по студентам")
        for student in self.students:
            if student.id == student_id:
                self.students.remove(student)
                return student
        raise Exception("Студент не найден")

    def search(self, text: str) -> list[Student]:
        found_students = [student for student in self.students if text.lower() in student.full_name.lower()]
        print(self.__print_student(found_students))
        return found_students

    def __len__(self) -> int:
        return len(self.students)

    def __repr__(self) -> str:
        return self.__print_student(self.students)

    @staticmethod
    def __print_student(students: list[Student]) -> str:
        return '\n'.join([str(student) for student in students])
