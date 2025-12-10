from app.database import init_db

def setup_module(module):
    # This is called once before any tests in this file run
    init_db()

import pytest
from app.database import get_db_session, log_event
from app.model import EventLog

def test_log_event():
    session = get_db_session()
    
    # Log a sample event
    features = [1, 2, 3]
    is_anomaly = True
    log_event(session, features, is_anomaly)
    
    # Query the logged event
    event = session.query(EventLog).order_by(EventLog.id.desc()).first()
    
    assert event.features == str(features)
    assert event.is_anomaly == is_anomaly
    
    # Clean up test data
    session.delete(event)
    session.commit()
