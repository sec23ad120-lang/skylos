from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Base, EventLog

DATABASE_URL = "sqlite:///./skylos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    return SessionLocal()

def log_event(db_session, features, is_anomaly):
    log = EventLog(features=str(features), is_anomaly=is_anomaly)
    db_session.add(log)
    db_session.commit()
