import numpy as np

from app.ai.features import extract_features
from app.ai.hybrid_detector import HybridAnomalyDetector


def load_normal_events() -> list[dict]:
    """
    TEMP data: replace with real normal logs later.
    These are example 'normal' events.
    """
    return [
        {"failed_logins": 0, "successful_logins": 10, "bytes_in": 1000, "bytes_out": 900},
        {"failed_logins": 1, "successful_logins": 8, "bytes_in": 1500, "bytes_out": 1200},
        {"failed_logins": 0, "successful_logins": 12, "bytes_in": 3000, "bytes_out": 2500},
    ]


def main():
    normal_events = load_normal_events()
    X_norm = np.array([extract_features(e) for e in normal_events], dtype="float32")

    detector = HybridAnomalyDetector()

    # 1) train IsolationForest
    detector.train_isolation_forest(X_norm)

    # 2) train deep autoencoder
    detector.train_deep_autoencoder(X_norm, epochs=10, batch_size=2)


if __name__ == "__main__":
    main()