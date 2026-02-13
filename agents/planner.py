# planner.py

import time
from trusta2a.router import trust_router
from trusta2a.aic import sign_message
from registry import AGENT_SECRETS


SENDER_ID = "planner_1"


def send_task(receiver_id: str, content: str) -> dict:
    timestamp = time.time()
    intent = "task"

    payload = f"{SENDER_ID}|{receiver_id}|{content}|{timestamp}|{intent}"
    signature = sign_message(AGENT_SECRETS[SENDER_ID], payload)

    message = {
        "sender_id": SENDER_ID,
        "receiver_id": receiver_id,
        "content": content,
        "timestamp": timestamp,
        "intent": intent,
        "risk_metadata": {},
        "signature": signature
    }

    return trust_router(message)
