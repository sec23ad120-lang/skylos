import pytest
from app.ai.predictive_analytics import PredictiveAnalytics
from app.model import EventLog
from app.database import get_db_session
import datetime

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

@pytest.fixture(scope="module")
def predictive_analytics(setup_dummy_events):
    pa = PredictiveAnalytics()
    pa.train()
    return pa

def test_training_and_prediction(predictive_analytics):
    prediction = predictive_analytics.predict(3)
    assert isinstance(prediction, int)
    assert prediction >= 0

def test_prepare_data():
    pa = PredictiveAnalytics()
    day1 = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    day2 = day1 + datetime.timedelta(days=1)

    events = [
        EventLog(id=1, features="feat1", is_anomaly=True, timestamp=day1),
        EventLog(id=2, features="feat2", is_anomaly=True, timestamp=day1),
        EventLog(id=3, features="feat3", is_anomaly=False, timestamp=day2),
        EventLog(id=4, features="feat4", is_anomaly=True, timestamp=day2),
    ]

    X, y = pa.prepare_data(events)
    assert X.shape[0] == len(set([e.timestamp.date() for e in events if e.is_anomaly]))
    assert y.sum() == 3
