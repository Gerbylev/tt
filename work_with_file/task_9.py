import os
import tempfile
from dataclasses import dataclass

@dataclass
class Student:
    surname: str
    birth_year: int
    group: str
    avg_grade: float
    enrollment_year: int

# Определить средний возраст для каждой группы
# Найти всех кто меньше медианы
# Сформировать список самых высоких средних групп


def read_students(filename):
    students = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) != 5:
                continue
            surname, birth_year, group, avg_grade, enrollment_year = parts
            try:
                student = Student(surname, int(birth_year), group, float(avg_grade), int(enrollment_year))
                students.append(student)
            except ValueError:
                continue
    return students

def get_common_surnames(students):
    surname_dict = {}
    for student in students:
        surname_dict.setdefault(student.surname, []).append(student)
    return {surname: lst for surname, lst in surname_dict.items() if len(lst) > 1}

def get_round_excellents(students):
    return [student for student in students if student.avg_grade == 5.0]

def group_students_by_group(students):
    groups = {}
    for student in students:
        groups.setdefault(student.group, []).append(student)
    return groups

def get_group_with_max_students(students):
    groups = group_students_by_group(students)
    max_group = None
    max_count = 0
    for group, lst in groups.items():
        if len(lst) > max_count:
            max_count = len(lst)
            max_group = group
    return max_group

def get_group_with_max_excellents(students):
    groups = group_students_by_group(students)
    max_group = None
    max_count = 0
    for group, lst in groups.items():
        count = sum(1 for student in lst if student.avg_grade == 5.0)
        if count > max_count:
            max_count = count
            max_group = group
    return max_group

def get_group_median_age(students):
    groups = group_students_by_group(students)
    groups_median_age = {}
    for group, lst in groups.items():
        groups_median_age[group] = sum([student.birth_year for student in lst])/len(lst)
    return groups_median_age

def get_student_age_less(students):
    groups = group_students_by_group(students)
    res = []
    for group, lst in groups.items():
        median_age = sum([student.birth_year for student in lst]) / len(lst)
        for student in lst:
            if student.birth_year < median_age:
                res.append(student)
    return res

def create_group_files(students, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    groups = group_students_by_group(students)
    for group, lst in groups.items():
        filename = os.path.join(output_dir, f"group_{group}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            for student in lst:
                f.write(f"{student.surname} {student.birth_year} {student.group} {student.avg_grade} {student.enrollment_year}\n")

def age_work():
    student_data = """Ivanov 1999 101 4.5 2017
Petrov 2000 101 4.0 2018
Petrov 2005 101 4.0 2018
Petrov 2006 101 4.0 2018
Petrov 1982 101 4.0 2018
Petrov 1982 101 4.0 2018
Sidorov 1998 102 3.5 2016
Smirnov 2001 102 4.8 2019
"""
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
        tmp.write(student_data)
    students = read_students(tmp.name)
    os.unlink(tmp.name)
    common = get_common_surnames(students)
    median_age = get_group_median_age(students)
    for group, age in median_age.items():
        print(f"Для группы {group}  средний возраст {age:.2f}")
    age_less_student = get_student_age_less(students)
    for student in age_less_student:
        print(f"В группе {student.group} средний возраст {median_age[student.group]:.2f} возраст студента {student.birth_year}, Студент {student}")
    # print(age_less_student)

if __name__ == "__main__":
    age_work()

# def test_task9_case1():
#     student_data = "Ivanov 1999 101 5.0 2017\n"
#     with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
#         tmp.write(student_data)
#     students = read_students(tmp.name)
#     os.unlink(tmp.name)
#     common = get_common_surnames(students)
#     assert common == {}, "Ожидается отсутствие однофамильцев при одном студенте"
#     round_excellents = get_round_excellents(students)
#     assert len(round_excellents) == 1, "Ожидается 1 отличник"
#     groups = group_students_by_group(students)
#     assert groups == {"101": students}, "Ожидается только группа 101"
#     assert get_group_with_max_students(students) == "101", "Группа с макс. числом студентов – 101"
#     assert get_group_with_max_excellents(students) == "101", "Группа с макс. числом отличников – 101"
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         create_group_files(students, tmp_dir)
#         filename = os.path.join(tmp_dir, "group_101.txt")
#         assert os.path.exists(filename), "Файл для группы 101 не найден"
#
# def test_task9_case2():
#     student_data = """Ivanov 1999 101 4.5 2017
# Petrov 2000 101 4.0 2018
# Sidorov 1998 102 3.5 2016
# Smirnov 2001 102 4.8 2019
# """
#     with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
#         tmp.write(student_data)
#     students = read_students(tmp.name)
#     os.unlink(tmp.name)
#     common = get_common_surnames(students)
#     assert common == {}, "Ожидается отсутствие однофамильцев"
#     round_excellents = get_round_excellents(students)
#     assert len(round_excellents) == 0, "Отличников не должно быть"
#     groups = group_students_by_group(students)
#     assert len(groups) == 2, "Ожидается 2 группы"
#     max_group = get_group_with_max_students(students)
#     assert max_group in groups, "Неверно определена группа с макс. числом студентов"
#     max_excellent_group = get_group_with_max_excellents(students)
#     assert max_excellent_group not in groups, "Неверно определена группа с макс. числом отличников"
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         create_group_files(students, tmp_dir)
#         for group in groups:
#             filename = os.path.join(tmp_dir, f"group_{group}.txt")
#             assert os.path.exists(filename), f"Файл для группы {group} не найден"
#
# def test_task9_case3():
#     student_data = """Ivanov 1999 101 5.0 2017
# Petrov 2000 101 5.0 2018
# Sidorov 1998 102 5.0 2016
# Smirnov 2001 102 5.0 2019
# """
#     with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
#         tmp.write(student_data)
#         tmp.close()
#         students = read_students(tmp.name)
#         os.unlink(tmp.name)
#     common = get_common_surnames(students)
#     assert common == {}, "При уникальных фамилиях однофамильцев не должно быть"
#     round_excellents = get_round_excellents(students)
#     assert len(round_excellents) == 4, "Все студенты – отличники"
#     groups = group_students_by_group(students)
#     assert len(groups) == 2, "Ожидается 2 группы"
#     max_group = get_group_with_max_students(students)
#     assert max_group in groups, "Неверно определена группа с макс. числом студентов"
#     max_excellent_group = get_group_with_max_excellents(students)
#     assert max_excellent_group in groups, "Неверно определена группа с макс. числом отличников"
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         create_group_files(students, tmp_dir)
#         for group in groups:
#             filename = os.path.join(tmp_dir, f"group_{group}.txt")
#             assert os.path.exists(filename), f"Файл для группы {group} не найден"
#
# def test_task9_case4():
#     student_data = """Ivanov 1999 101 5.0 2017
# InvalidLine
# Petrov 2000 101 4.5 2018 extra_field
# Sidorov 1998 102 5.0 2016
#    Smirnov   2001   102   4.8   2019
# """
#     with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
#         tmp.write(student_data)
#     students = read_students(tmp.name)
#     os.unlink(tmp.name)
#     assert len(students) == 3, "Ожидается 3 корректные записи студентов"
#     groups = group_students_by_group(students)
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         create_group_files(students, tmp_dir)
#         for group in groups:
#             filename = os.path.join(tmp_dir, f"group_{group}.txt")
#             assert os.path.exists(filename), f"Файл для группы {group} не найден"
#
# def run_all_task9_tests():
#     test_task9_case1()
#     test_task9_case2()
#     test_task9_case3()
#     test_task9_case4()

# if __name__ == '__main__':
#     run_all_task9_tests()
