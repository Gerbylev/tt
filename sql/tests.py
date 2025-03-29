from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import sessionmaker
from sql.dao.appointment import Appointment
from sql.dao.base import init_db, engine, Base
from sql.dao.doctor import Doctor
from sql.dao.patient import Patient
from sql.dao.treatment import Treatment
from sql.main import populate_data


@pytest.fixture(scope="function")
def session():
    init_db()
    _sessionmaker = sessionmaker(bind=engine)
    session = _sessionmaker()
    populate_data(session)
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_query_all_doctors(session):
    doctors = Doctor.query_all_doctors(session)
    assert len(doctors) == 3, f"Ожидалось 3 врача, получено {len(doctors)}"
    for doc in doctors:
        assert doc.name, "Имя врача не должно быть пустым"

def test_query_all_doctors_empty_db(session):
    session.query(Doctor).delete()
    session.commit()
    doctors = Doctor.query_all_doctors(session)
    assert len(doctors) == 0, "Ожидалось 0 врачей при пустой базе данных"

def test_query_all_patients(session):
    patients = Patient.query_all_patients(session)
    assert len(patients) == 3, f"Ожидалось 3 пациента, получено {len(patients)}"
    for pat in patients:
        assert pat.email, "Email пациента не должен быть пустым"

def test_query_all_patients_empty_db(session):
    session.query(Patient).delete()
    session.commit()
    patients = Patient.query_all_patients(session)
    assert len(patients) == 0, "Ожидалось 0 пациентов при пустой базе данных"

def test_query_appointments_by_doctor(session):
    appts = Appointment.query_appointments_by_doctor(session, 1)
    assert len(appts) == 3, f"Ожидалось 3 приёма для врача id=1, получено {len(appts)}"
    for a in appts:
        assert a.doctor_id == 1, "Приём не принадлежит врачу с id=1"

def test_query_appointments_by_doctor_no_appointments(session):
    appts = Appointment.query_appointments_by_doctor(session, doctor_id=999)
    assert len(appts) == 0, "Ожидалось 0 приёмов для несуществующего врача"

def test_query_appointments_in_date_range(session):
    now = datetime.now()
    start = now - timedelta(days=15)
    end = now - timedelta(days=1)
    appts = Appointment.query_appointments_in_date_range(session, start, end)
    assert len(appts) >= 1, "Ожидался хотя бы 1 приём в указанном диапазоне"
    for a in appts:
        assert start <= a.appointment_date <= end, "Дата приёма выходит за заданный диапазон"

def test_query_appointments_in_date_range_empty_range(session):
    start = datetime.now() + timedelta(days=100)
    end = datetime.now() + timedelta(days=101)
    appts = Appointment.query_appointments_in_date_range(session, start, end)
    assert len(appts) == 0, "Ожидалось 0 приёмов для пустого диапазона дат"

def test_query_doctors_by_specialization(session):
    docs = Doctor.query_doctors_by_specialization(session, "Терапевт")
    assert len(docs) >= 1, "Не найден ни один терапевт"
    for d in docs:
        assert d.specialization == "Терапевт", "Специализация не соответствует запросу"

def test_query_doctors_by_specialization_nonexistent(session):
    docs = Doctor.query_doctors_by_specialization(session, "Нейрохирург")
    assert len(docs) == 0, "Ожидалось 0 врачей для несуществующей специализации"

def test_create_appointment(session):
    new_date = datetime.now() + timedelta(days=7)
    appt = Appointment.create_appointment(session, 1, 2, new_date, "Новый приём")
    assert appt.id is not None, "Новый приём не получил id"
    found = session.query(Appointment).filter(Appointment.id == appt.id).first()
    assert found is not None, "Новый приём не найден в базе"

def test_create_appointment_new_data(session):
    Appointment.create_appointment(session, patient_id=999, doctor_id=999, app_date=datetime.now(), reason="Тест")

def test_update_appointment_reason(session):
    appt = session.query(Appointment).first()
    old_reason = appt.reason
    updated = Appointment.update_appointment_reason(session, appt.id, "Обновлённая причина")
    assert updated.reason == "Обновлённая причина", "Причина не обновлена"
    appt_check = session.query(Appointment).filter(Appointment.id == appt.id).first()
    assert appt_check.reason == "Обновлённая причина", "Изменение не сохранено в базе"

def test_update_appointment_reason_nonexistent(session):
    updated = Appointment.update_appointment_reason(session, appointment_id=999, new_reason="Обновлённая причина")
    assert updated is None, "Ожидалось None для несуществующего приёма"

def test_delete_appointment(session):
    new_date = datetime.now() + timedelta(days=2)
    temp_appt = Appointment.create_appointment(session, 2, 3, new_date, "Временный приём")
    result = Appointment.delete_appointment(session, temp_appt.id)
    assert result, "Приём не был удалён"
    deleted = session.query(Appointment).filter(Appointment.id == temp_appt.id).first()
    assert deleted is None, "Приём всё ещё присутствует в базе"

def test_delete_appointment_nonexistent(session):
    result = Appointment.delete_appointment(session, appointment_id=999)
    assert not result, "Ожидалось False для несуществующего приёма"

def test_count_appointments_by_doctor(session):
    counts = Appointment.count_appointments_by_doctor(session)
    for name, cnt in counts:
        assert isinstance(name, str) and isinstance(cnt, int), "Неверный формат данных"
    total_appts = session.query(Appointment).count()
    sum_counts = sum([cnt for _, cnt in counts])
    assert total_appts == sum_counts, "Суммарное число приёмов не совпадает"

def test_count_appointments_by_doctor_no_appointments(session):
    counts = Appointment.count_appointments_by_doctor(session)
    for name, cnt in counts:
        if name == "Сидорова Анна":
            assert cnt == 1, "Ожидался 1 приём для врача с id=3"
        elif name == "Иванов Иван":
            assert cnt == 3, "Ожидалось 3 приёма для врача с id=1"
        elif name == "Петров Пётр":
            assert cnt == 1, "Ожидался 1 приём для врача с id=2"

def test_query_appointment_details(session):
    details = Appointment.query_appointment_details(session)
    for rec in details:
        assert rec.patient_name and rec.doctor_name and rec.reason, "Запись не содержит всех данных"
    assert len(details) >= 1, "Ожидалось наличие хотя бы одной записи"

def test_query_appointment_details_empty_db(session):
    session.query(Appointment).delete()
    session.commit()
    details = Appointment.query_appointment_details(session)
    assert len(details) == 0, "Ожидалось 0 записей при пустой базе данных"

def test_query_treatments_by_appointment(session):
    appt = session.query(Appointment).filter(Appointment.treatments != None).first()
    if appt:
        treatments = Treatment.query_treatments_by_appointment(session, appt.id)
        assert len(treatments) >= 1, "Ожидалось наличие лечения для данного приёма"
    treatments_none = Treatment.query_treatments_by_appointment(session, -1)
    assert treatments_none == [], "Ожидался пустой список для несуществующего приёма"

def test_query_treatments_by_appointment_no_treatments(session):
    treatments = Treatment.query_treatments_by_appointment(session, appointment_id=8)
    assert len(treatments) == 0, "Ожидалось 0 лечений для приёма без лечения"

