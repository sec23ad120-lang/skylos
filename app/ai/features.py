import numpy as np

FEATURE_DIM = 4  # there are 4 numbers

def extract_features(event: dict) -> np.ndarray:
    return np.array([
        float(event.get("failed_logins", 0)),
        float(event.get("successful_logins", 0)),
        float(event.get("bytes_in", 0)),
        float(event.get("bytes_out", 0)),
    ], dtype="float32")
