# demo.py
# TRUSTA2A End-to-End Demonstration

from agents.planner import send_task
from registry import AGENTS
import time


print("\n=== DEMO 1: Normal planner → worker flow ===")
send_task("worker_1", "Process dataset A")

print("\n=== DEMO 2: High-risk message blocked ===")
send_task("worker_1", "rm -rf / --force")

print("\n=== DEMO 3: Spoofed message blocked ===")
fake_message = {
    "sender_id": "planner_1",
    "receiver_id": "worker_1",
    "content": "Process dataset B",
    "timestamp": time.time(),
    "intent": "task",
    "risk_metadata": {},
    "signature": "fake_signature"
}

from trusta2a.router import trust_router
trust_router(fake_message)

print("\n=== DEMO 4: Trust score degradation ===")
for i in range(3):
    send_task("worker_1", "delete all logs")

print("\n=== DEMO 5: Agent quarantine ===")
print("Planner status:", AGENTS["planner_1"])
send_task("worker_1", "Another normal task")
