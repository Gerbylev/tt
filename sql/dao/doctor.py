from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from sql.dao.base import Base

class Doctor(Base):
    __tablename__ = 'doctors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    specialization: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String)

    appointments: Mapped[List['Appointment']] = relationship(back_populates="doctor")

    @staticmethod
    def query_all_doctors(session) -> list['Doctor']:
        return session.query(Doctor).all()

    @staticmethod
    def query_doctors_by_specialization(session, specialization) -> list['Doctor']:
        return session.query(Doctor).filter(Doctor.specialization == specialization).all()