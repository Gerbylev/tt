from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column


from sql.dao.base import Base


class Patient(Base):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[DateTime] = mapped_column(DateTime)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    appointments: Mapped[List['Appointment']] = relationship(back_populates="patient")

    @staticmethod
    def query_all_patients(session) -> list['Patient']:
        return session.query(Patient).all()