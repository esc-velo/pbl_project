# registry.py
# Static agent registry (NO LOGIC)

AGENTS = {
    "planner_1": {
        "id": "planner_1",
        "role": "planner",
        "trust": 0.8,
        "status": "active"
    },
    "worker_1": {
        "id": "worker_1",
        "role": "worker",
        "trust": 0.7,
        "status": "active"
    },
    "safety_1": {
        "id": "safety_1",
        "role": "safety",
        "trust": 0.9,
        "status": "active"
    }
}

AGENT_SECRETS = {
    "planner_1": "planner_secret_key",
    "worker_1": "worker_secret_key",
    "safety_1": "safety_secret_key"
}
