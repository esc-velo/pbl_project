# trust.py
# Dynamic Trust Score (DTS)

from registry import AGENTS


def clamp_trust(value: float) -> float:
    return max(0.0, min(1.0, value))


def update_trust(agent_id: str, event: str) -> None:
    agent = AGENTS.get(agent_id)
    if not agent:
        return

    delta = 0.0

    if event == "safe_action":
        delta = 0.05
    elif event == "high_risk_blocked":
        delta = -0.20
    elif event == "serious_violation":
        delta = -0.50

    agent["trust"] = clamp_trust(agent["trust"] + delta)

    if agent["trust"] < 0.1:
        agent["status"] = "quarantined"
