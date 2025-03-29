from typing import List, Tuple

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from sql.dao.base import Base
from sql.dao.doctor import Doctor
from sql.dao.patient import Patient
from sql.dao.treatment import Treatment


class Appointment(Base):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    doctor_id: Mapped[int] = mapped_column(ForeignKey('doctors.id'))
    appointment_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    reason: Mapped[str] = mapped_column(String)

    patient: Mapped['Patient'] = relationship(back_populates="appointments")
    doctor: Mapped['Doctor'] = relationship(back_populates="appointments")
    treatments: Mapped[List['Treatment']] = relationship(back_populates="appointment")

    @staticmethod
    def query_appointments_in_date_range(session, start_date, end_date) -> list['Appointment']:
        return session.query(Appointment).filter(Appointment.appointment_date.between(start_date, end_date)).all()

    @staticmethod
    def create_appointment(session, patient_id, doctor_id, app_date, reason):
        new_appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_date=app_date, reason=reason)
        session.add(new_appt)
        session.commit()
        return new_appt

    @staticmethod
    def query_appointments_by_doctor(session, doctor_id) -> list['Appointment']:
        return session.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    @staticmethod
    def update_appointment_reason(session, appointment_id, new_reason) -> 'Appointment':
        appt = session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appt:
            appt.reason = new_reason
            session.commit()
        return appt

    @staticmethod
    def delete_appointment(session, appointment_id) -> bool:
        appt = session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appt:
            session.delete(appt)
            session.commit()
            return True
        return False

    @staticmethod
    def count_appointments_by_doctor(session) -> list[Tuple[str, int]]:
        return session.query(Doctor.name, func.count(Appointment.id)).join(Appointment).group_by(Doctor.id).all()

    @staticmethod
    def query_appointment_details(session):
        return session.query(
            Appointment.id,
            Patient.name.label("patient_name"),
            Doctor.name.label("doctor_name"),
            Appointment.appointment_date,
            Appointment.reason
        ).join(Patient, Appointment.patient_id == Patient.id
               ).join(Doctor, Appointment.doctor_id == Doctor.id).all()