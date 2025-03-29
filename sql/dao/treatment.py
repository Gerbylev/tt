from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


from sql.dao.base import Base


class Treatment(Base):
    __tablename__ = 'treatments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey('appointments.id'))
    description: Mapped[str] = mapped_column(String)
    cost: Mapped[int] = mapped_column(Integer)

    appointment: Mapped['Appointment'] = relationship(back_populates="treatments")

    @staticmethod
    def query_treatments_by_appointment(session, appointment_id):
        return session.query(Treatment).filter(Treatment.appointment_id == appointment_id).all()