import pytest
from app.ai.anomaly_detector import AnomalyDetector

def test_train_and_predict():
    detector = AnomalyDetector()
    # Dummy data representing normal events
    data = [[0, 0], [1, 1], [0.1, 0.1]]
    detector.train(data)
    
    assert detector.predict([0, 0]) == False  # Normal
    assert detector.predict([10, 10]) == True  # Anomaly

from app.ai.anomaly_detector import process_event

def test_process_event():
    event = {
        "source_ip": "192.168.1.100",
        "description": "Multiple failed login attempts detected",
        "timestamp": "2025-09-21T20:45:00Z",
        "field1": 999,
        "field2": 123,
        # other features as needed
    }
    process_event(event)
    print("Test event processed. Verify alerts and logs.")
