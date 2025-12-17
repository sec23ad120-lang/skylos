import numpy as np
from app.ai.features import extract_features          # <-- new
from app.ai.hybrid_detector import HybridAnomalyDetector  # <-- new

from app.security.automated_response import AutomatedResponse


# Set up the hybrid detector ONCE when the app starts
hybrid_detector = HybridAnomalyDetector()
hybrid_detector.load_isolation_forest()
hybrid_detector.load_deep_autoencoder()

response_handler = AutomatedResponse()


def is_anomaly(event: dict) -> bool:
    """
    Use the hybrid model (IsolationForest + autoencoder)
    to decide if this event is anomalous.
    """
    is_anom, scores = hybrid_detector.predict_event(event)
    # you can log 'scores' if you want later
    return is_anom


def process_event(event: dict):
    """
    Main function: called whenever a new event comes in.
    If it's an anomaly, trigger the automated response.
    """
    if is_anomaly(event):
        anomaly_info = {
            "source_ip": event.get("source_ip"),
            "description": event.get("description", "Anomaly detected"),
            "timestamp": event.get("timestamp"),
        }
        response_handler.handle_anomaly(anomaly_info)
        # Continue with logging or other processing
