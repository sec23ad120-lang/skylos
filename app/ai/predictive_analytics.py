from typing import List, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime
from app.model import EventLog
from app.database import get_db_session


class PredictiveAnalytics:
    def __init__(self):
        self.model = LinearRegression()

    def prepare_data(self, events: List[EventLog]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Converts event logs to numeric X, y data for regression.
        X: day index (int), y: count of anomalies per day
        """
        # Group events by day and count anomalies
        day_counts = {}
        for event in events:
            if event.is_anomaly:
                day = event.timestamp.date()
                day_counts[day] = day_counts.get(day, 0) + 1

        # Sort by day
        sorted_days = sorted(day_counts.keys())
        X = np.array([(day - sorted_days[0]).days for day in sorted_days]).reshape(-1, 1)
        y = np.array([day_counts[day] for day in sorted_days])

        return X, y

    def train(self):
        # Load events from DB
        session = get_db_session()
        events = session.query(EventLog).all()

        if not events:
            raise ValueError("No event data found for training")

        X, y = self.prepare_data(events)
        if len(X) < 2:
            raise ValueError("Not enough data for training")

        self.model.fit(X, y)

    def predict(self, days_ahead: int) -> int:
        """
        Predict anomaly count days_ahead (int).
        """
        last_day_index = 0
        prediction_input = np.array([[last_day_index + days_ahead]])
        pred = self.model.predict(prediction_input)
        return max(0, int(pred[0]))  # anomaly count can't be negative

import datetime
import pytest
from app.model import EventLog
from app.database import get_db_session

@pytest.fixture(scope="module")
def setup_dummy_events():
    session = get_db_session()
    base_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(3):
        for _ in range(i+1):
            event = EventLog(
                features="dummy",
                is_anomaly=True,
                timestamp=base_date + datetime.timedelta(days=i)
            )
            session.add(event)
    session.commit()
    yield
    session.query(EventLog).delete()
    session.commit()
