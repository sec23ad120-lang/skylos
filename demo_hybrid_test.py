from app.ai.anomaly_detector import process_event, is_anomaly

normal_event = {
    "source_ip": "10.0.0.5",
    "description": "Normal user activity",
    "timestamp": "2025-12-10T19:30:00Z",
    "failed_logins": 0,
    "successful_logins": 12,
    "bytes_in": 1500,
    "bytes_out": 1200,
}

attack_event = {
    "source_ip": "203.0.113.99",
    "description": "Suspicious login storm",
    "timestamp": "2025-12-10T19:31:00Z",
    "failed_logins": 40,
    "successful_logins": 1,
    "bytes_in": 50000,
    "bytes_out": 200,
}

print("Normal event anomalous? ", is_anomaly(normal_event))
print("Attack event anomalous? ", is_anomaly(attack_event))

# Also run full pipeline (this will call AutomatedResponse for anomalies)
process_event(normal_event)
process_event(attack_event)
