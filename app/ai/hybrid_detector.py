import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

from tensorflow import keras
from tensorflow.keras import layers

from app.ai.features import extract_features, FEATURE_DIM


class HybridAnomalyDetector:
    def __init__(
        self,
        iso_model_path: str = "models/isolation_forest.joblib",
        dl_model_path: str = "models/dl_autoencoder.keras",
        dl_threshold_path: str = "models/dl_threshold.npy",
    ):
        self.iso_model_path = iso_model_path
        self.dl_model_path = dl_model_path
        self.dl_threshold_path = dl_threshold_path

        self.iforest: IsolationForest | None = None
        self.dl_model: keras.Model | None = None
        self.dl_threshold: float | None = None

    # ---------- IsolationForest ----------

    def train_isolation_forest(self, X_norm: np.ndarray) -> None:
        self.iforest = IsolationForest(
            n_estimators=200,
            contamination=0.05,
            random_state=42,
        )
        self.iforest.fit(X_norm)
        joblib.dump(self.iforest, self.iso_model_path)

    def load_isolation_forest(self) -> None:
        self.iforest = joblib.load(self.iso_model_path)

    def iforest_score(self, x: np.ndarray) -> float:
        if self.iforest is None:
            raise RuntimeError("IsolationForest not loaded")
        x = x.reshape(1, -1)
        return float(-self.iforest.score_samples(x)[0])

    # ---------- Deep autoencoder (TensorFlow) ----------

    def _build_autoencoder(self) -> keras.Model:
        inputs = keras.Input(shape=(FEATURE_DIM,), name="features")
        x = layers.Dense(32, activation="relu")(inputs)
        x = layers.Dense(16, activation="relu")(x)
        latent = layers.Dense(8, activation="relu", name="latent")(x)
        x = layers.Dense(16, activation="relu")(latent)
        x = layers.Dense(32, activation="relu")(x)
        outputs = layers.Dense(FEATURE_DIM, activation="linear")(x)

        model = keras.Model(inputs, outputs, name="tabular_autoencoder")
        model.compile(optimizer="adam", loss="mse")
        return model

    def train_deep_autoencoder(self, X_norm: np.ndarray, epochs: int = 30, batch_size: int = 32) -> None:
        X_norm = X_norm.astype("float32")

        model = self._build_autoencoder()
        model.fit(
            X_norm,
            X_norm,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_split=0.1,
            verbose=1,
        )

        X_pred = model.predict(X_norm, verbose=0)
        errors = np.mean(np.square(X_norm - X_pred), axis=1)
        threshold = float(np.percentile(errors, 95))

        model.save(self.dl_model_path)
        np.save(self.dl_threshold_path, np.array(threshold, dtype="float32"))

        self.dl_model = model
        self.dl_threshold = threshold

    def load_deep_autoencoder(self) -> None:
        self.dl_model = keras.models.load_model(self.dl_model_path)
        self.dl_threshold = float(np.load(self.dl_threshold_path))

    def dl_reconstruction_error(self, x: np.ndarray) -> float:
        if self.dl_model is None or self.dl_threshold is None:
            raise RuntimeError("Deep autoencoder not loaded")
        x = x.astype("float32").reshape(1, -1)
        x_pred = self.dl_model.predict(x, verbose=0)
        err = float(np.mean(np.square(x - x_pred)))
        return err

    # ---------- Hybrid decision ----------

    def predict_event(self, event: dict):
        features = extract_features(event)
        if features.shape[0] != FEATURE_DIM:
            raise ValueError(f"Expected feature dim {FEATURE_DIM}, got {features.shape[0]}")

        if_score = self.iforest_score(features)
        dl_error = self.dl_reconstruction_error(features)

        IF_THRESHOLD = 0.5
        DL_THRESHOLD = self.dl_threshold

        is_anom = (if_score > IF_THRESHOLD) or (dl_error > DL_THRESHOLD)

        return is_anom, {
            "iforest_score": if_score,
            "dl_error": dl_error,
            "iforest_threshold": IF_THRESHOLD,
            "dl_threshold": DL_THRESHOLD,
        }
