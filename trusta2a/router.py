# router.py
# TRUSTA2A Core Router

import time
from registry import AGENTS, AGENT_SECRETS
from trusta2a.aic import verify_signature
from trusta2a.trust import update_trust
from trusta2a.risk import assess_risk

from agents.worker import handle_message as worker_handle
from agents.safety import handle_message as safety_handle


def trust_router(message: dict) -> dict:
    sender_id = message.get("sender_id")
    receiver_id = message.get("receiver_id")

    print(f"\n[ROUTER] Message from {sender_id} → {receiver_id}")

    sender = AGENTS.get(sender_id)
    receiver = AGENTS.get(receiver_id)

    if not sender or not receiver:
        print("[ROUTER] ❌ Unknown agent identity")
        return {"status": "rejected", "reason": "Unknown agent"}

    if sender["status"] != "active":
        print("[ROUTER] ❌ Sender is quarantined")
        return {"status": "rejected", "reason": "Sender quarantined"}

    payload = f"{sender_id}|{receiver_id}|{message['content']}|{message['timestamp']}|{message['intent']}"

    secret = AGENT_SECRETS.get(sender_id)
    if not verify_signature(secret, payload, message["signature"]):
        print("[ROUTER] ❌ Signature verification failed (spoofing detected)")
        update_trust(sender_id, "serious_violation")
        return {"status": "rejected", "reason": "Invalid signature"}

    risk = assess_risk(message, sender, receiver)
    print(f"[ROUTER] Risk assessment: {risk['risk_level']}")

    if risk["risk_level"] == "high":
        print("[ROUTER] ❌ High-risk message blocked")
        update_trust(sender_id, "high_risk_blocked")
        return {"status": "blocked", "reason": risk["reasons"]}

    # Forward message
    if receiver["role"] == "worker":
        response = worker_handle(message)
    elif receiver["role"] == "safety":
        response = safety_handle(message)
    else:
        response = {"status": "delivered"}

    update_trust(sender_id, "safe_action")
    print("[ROUTER] ✅ Message delivered successfully")

    return response
