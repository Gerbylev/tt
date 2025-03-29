from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

engine = create_engine('sqlite:///:memory:', echo=False)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_session() -> Session:
    return SessionLocal()


def init_db():
    Base.metadata.create_all(bind=engine)