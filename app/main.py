from fastapi import FastAPI, Request
from app.security1 import check_access, encrypt_data
from app.ai.anomaly_detector import AnomalyDetector
from app.database import get_db_session, log_event
from app.security import data_encryption
app = FastAPI(title="Skylos")

@app.post("/log_query/")
async def log_query(request: Request):
    data = await request.json()
    db_session = get_db_session()
    # Logging and anomaly check
    is_anomaly = AnomalyDetector(data)
    log_event(db_session, data, is_anomaly)
    if is_anomaly:
        # Respond to threat automatically
        return {"status": "alert", "message": "Anomaly detected. Automated response triggered."}
    return {"status": "ok"}

@app.post("/access_data/")
async def access_data(request: Request):
    data = await request.json()
    if not check_access(data["user"], data["resource"]):
        return {"status": "denied"}
    # Encrypt before responding
    encrypted = encrypt_data(data["payload"])
    return {"status": "success", "data": encrypted}

from fastapi import APIRouter
from app.ai.predictive_analytics import PredictiveAnalytics

router = APIRouter()

predictive_analytics = PredictiveAnalytics()


@router.get("/predict_anomalies/")
async def predict_anomalies(days_ahead: int):
    count = predictive_analytics.predict(days_ahead)
    return {"predicted_anomaly_count": count}

from app.security.data_encryption import DataEncryption

encryptor = DataEncryption()
@app.post("/access_data/")
async def access_data(request: Request):
    data = await request.json()
    if not check_access(data["user"], data["resource"]):
        return {"status": "denied"}
    # Encrypt before responding
    encrypted = encryptor.encrypt(data["payload"].encode())
    return {"status": "success", "data": encrypted.decode()}

@app.get("/decrypt_data/")
async def decrypt_data(request: Request):
    encrypted_payload = (await request.json())["encrypted"]
    decrypted = encryptor.decrypt(encrypted_payload.encode()).decode()
    return {"decrypted_data": decrypted}
