import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

    def train(self, data):
        self.model.fit(data)
        joblib.dump(self.model, "anomaly_detector_model.joblib")

    def load_model(self, path="anomaly_detector_model.joblib"):
        self.model = joblib.load(path)

    def predict(self, features):
        arr = np.array(features).reshape(1, -1)
        prediction = self.model.predict(arr)
        return prediction[0] == -1
# Instantiate your anomaly detector and load the model
anomaly_detector = AnomalyDetector()
anomaly_detector.load_model()

def extract_features(event):
    # Example: adapt this to your real event structure and feature needs.
    # Return a list/array of numerical features for the model.
    return [
        float(event.get("field1", 0)),
        float(event.get("field2", 0))
        # Add more fields as required by your trained model
    ]

def is_anomaly(event):
    features = extract_features(event)
    return anomaly_detector.predict(features)

from app.security.automated_response import AutomatedResponse

response_handler = AutomatedResponse()

def process_event(event):
    if is_anomaly(event):
        anomaly_info = {
            "source_ip": event.get("source_ip"),
            "description": event.get("description", "Anomaly detected"),
            "timestamp": event.get("timestamp")
        }
        response_handler.handle_anomaly(anomaly_info)
        # Continue with logging or other processing
