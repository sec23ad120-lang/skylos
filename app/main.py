from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Hybrid Intrusion Detection API",
    description="Simple API to ingest events, access data, block IPs, and send feedback.",
    version="1.0.0",
)


# ---------- Data models ----------

class Event(BaseModel):
    source_ip: str
    description: str
    timestamp: str
    failed_logins: int
    successful_logins: int
    bytes_in: int
    bytes_out: int


class AccessRequest(BaseModel):
    user: str
    resource: str
    action: str
    extra: Optional[str] = None


class BlockRequest(BaseModel):
    ip: str
    reason: Optional[str] = None


class FeedbackRequest(BaseModel):
    event_id: str
    is_true_positive: bool
    comment: Optional[str] = None


# ---------- Simple root & health ----------

@app.get("/")
async def root():
    return {"message": "Hybrid IDS API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------- POST endpoints ----------

@app.post("/events/ingest")
async def ingest_event(event: Event):
    # TODO: plug in your hybrid anomaly detection logic here
    anomaly = (
        event.failed_logins > 10
        or event.bytes_in > 1000000
        or "attack" in event.description.lower()
    )

    decision = "block" if anomaly else "allow"

    return {
        "event": event,
        "anomaly": anomaly,
        "decision": decision,
        "message": "Event processed by hybrid IDS",
    }


@app.post("/access_data/")
async def access_data(body: AccessRequest):
    # TODO: replace with your real access control logic
    allowed = body.action.lower() in ["read", "view"]

    return {
        "user": body.user,
        "resource": body.resource,
        "action": body.action,
        "allowed": allowed,
        "reason": "Only read/view allowed in demo",
    }


@app.post("/block_ip/")
async def block_ip(body: BlockRequest):
    # TODO: here you would integrate with firewall or blocklist
    return {
        "ip": body.ip,
        "blocked": True,
        "reason": body.reason or "Blocked by IDS policy",
    }


@app.post("/feedback/")
async def feedback(body: FeedbackRequest):
    # TODO: here you would log feedback to a database to retrain/tune the model
    return {
        "event_id": body.event_id,
        "is_true_positive": body.is_true_positive,
        "comment": body.comment,
        "status": "feedback_received",
    }
