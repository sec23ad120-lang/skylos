import pytest
from app.ai.nlp_analysis import NLPClassifier

@pytest.fixture(scope="module")
def nlp_classifier():
    clf = NLPClassifier()

    # Add suspicious training samples
    clf.add_training_sample("unauthorized access attempt detected", 1)
    clf.add_training_sample("failed login from suspicious IP", 1)
    clf.add_training_sample("potential SQL injection attack", 1)

    # Add clean training samples
    clf.add_training_sample("user login successful", 0)
    clf.add_training_sample("profile updated successfully", 0)
    clf.add_training_sample("database query executed", 0)

    clf.train()
    return clf

def test_suspicious_prediction(nlp_classifier):
    assert nlp_classifier.predict("failed login from IP 192.168.1.100") == True
    assert nlp_classifier.predict("multiple unauthorized access attempts") == True

def test_clean_prediction(nlp_classifier):
    assert nlp_classifier.predict("user updated profile information") == False
    assert nlp_classifier.predict("database read operation completed") == False

def test_edge_empty_string(nlp_classifier):
    assert nlp_classifier.predict("") == False

def test_input_type(nlp_classifier):
    pred = nlp_classifier.predict("some log message")
    assert isinstance(pred, bool)
