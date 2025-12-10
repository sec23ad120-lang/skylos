from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class EventLog(Base):
    __tablename__ = 'event_logs'
    id = Column(Integer, primary_key=True)
    features = Column(String)
    is_anomaly = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)
