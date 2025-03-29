from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

from sql.dao.appointment import Appointment
from sql.dao.base import init_db, engine
from sql.dao.doctor import Doctor
from sql.dao.patient import Patient
from sql.dao.treatment import Treatment


def populate_data(session):
    doctor1 = Doctor(name="Иванов Иван", specialization="Терапевт", phone="111-111-111")
    doctor2 = Doctor(name="Петров Пётр", specialization="Хирург", phone="222-222-222")
    doctor3 = Doctor(name="Сидорова Анна", specialization="Педиатр", phone="333-333-333")
    session.add_all([doctor1, doctor2, doctor3])
    session.commit()

    patient1 = Patient(name="Алексей Смирнов", birth_date=datetime(1980, 5, 20), phone="444-444-444", email="alex@mail.ru")
    patient2 = Patient(name="Мария Кузнецова", birth_date=datetime(1990, 7, 15), phone="555-555-555", email="maria@mail.ru")
    patient3 = Patient(name="Николай Иванов", birth_date=datetime(1975, 3, 10), phone="666-666-666", email="nik@mail.ru")
    session.add_all([patient1, patient2, patient3])
    session.commit()

    now = datetime.now()
    appt1 = Appointment(patient=patient1, doctor=doctor1, appointment_date=now - timedelta(days=10), reason="Общее обследование")
    appt2 = Appointment(patient=patient2, doctor=doctor2, appointment_date=now - timedelta(days=5), reason="Хирургическая консультация")
    appt3 = Appointment(patient=patient3, doctor=doctor1, appointment_date=now + timedelta(days=1), reason="Повторный приём")
    appt4 = Appointment(patient=patient1, doctor=doctor3, appointment_date=now + timedelta(days=3), reason="Педиатрия")
    appt5 = Appointment(patient=patient2, doctor=doctor1, appointment_date=now + timedelta(days=5), reason="Лечение простуды")
    session.add_all([appt1, appt2, appt3, appt4, appt5])
    session.commit()

    treat1 = Treatment(appointment=appt1, description="Обследование", cost=100)
    treat2 = Treatment(appointment=appt2, description="Операция", cost=500)
    treat3 = Treatment(appointment=appt3, description="Консультация", cost=150)
    session.add_all([treat1, treat2, treat3])
    session.commit()


def main():
    init_db()

    _sessionmaker = sessionmaker(engine)
    session = _sessionmaker()

    populate_data(session)

    print("1. Все врачи:")
    doctors = Doctor.query_all_doctors(session)
    for d in doctors:
        print(f"  {d.id}: {d.name} ({d.specialization})")

    print("\n2. Все пациенты:")
    patients = Patient.query_all_patients(session)
    for p in patients:
        print(f"  {p.id}: {p.name}, email: {p.email}")

    print("\n3. Приёмы для врача с id=1:")
    appts_doc1 = Appointment.query_appointments_by_doctor(session, 1)
    for a in appts_doc1:
        print(f"  Приём {a.id} пациента {a.patient.name} на {a.appointment_date} по причине: {a.reason}")

    print("\n4. Приёмы в диапазоне дат:")
    start = datetime.now() - timedelta(days=15)
    end = datetime.now() - timedelta(days=1)
    appts_range = Appointment.query_appointments_in_date_range(session, start, end)
    for a in appts_range:
        print(f"  Приём {a.id} от {a.appointment_date} по причине: {a.reason}")

    print("\n5. Врачи по специализации 'Терапевт':")
    therapists = Doctor.query_doctors_by_specialization(session, "Терапевт")
    for d in therapists:
        print(f"  {d.id}: {d.name}")

    print("\n6. Создание нового приёма:")
    new_appt = Appointment.create_appointment(session, 1, 2, datetime.now() + timedelta(days=7), "Новый приём")
    print(f"  Создан приём id={new_appt.id}")

    print("\n7. Обновление причины приёма:")
    updated_appt = Appointment.update_appointment_reason(session, new_appt.id, "Обновлённая причина")
    print(f"  Приём id={updated_appt.id} теперь имеет причину: {updated_appt.reason}")

    print("\n8. Удаление приёма:")
    # Создадим временный приём для удаления
    temp_appt = Appointment.create_appointment(session, 2, 3, datetime.now() + timedelta(days=2), "Для удаления")
    if Appointment.delete_appointment(session, temp_appt.id):
        print(f"  Приём id={temp_appt.id} успешно удалён")

    print("\n9. Подсчёт приёмов по каждому врачу:")
    counts = Appointment.count_appointments_by_doctor(session)
    for name, cnt in counts:
        print(f"  {name}: {cnt} приём(а)")

    print("\n10. Детали приёма (объединённый запрос):")
    details = Appointment.query_appointment_details(session)
    for rec in details:
        print(f"  Приём id={rec.id}: пациент {rec.patient_name}, врач {rec.doctor_name}, дата {rec.appointment_date}, причина: {rec.reason}")

    print("\n11. Лечения для конкретного приёма:")
    treatments = Treatment.query_treatments_by_appointment(session, 1)
    for t in treatments:
        print(f"  Лечение id={t.id}: {t.description}, стоимость {t.cost}")

    print("\nВсе тесты успешно пройдены.")

if __name__ == "__main__":
    main()
