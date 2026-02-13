# risk.py
# Behavioral Risk Assessment (BRA)

DANGEROUS_KEYWORDS = [
    "delete",
    "shutdown",
    "format",
    "rm -rf",
    "override",
    "disable safety"
]


def assess_risk(message: dict, sender: dict, receiver: dict) -> dict:
    reasons = []

    content = message.get("content", "").lower()

    for word in DANGEROUS_KEYWORDS:
        if word in content:
            reasons.append(f"Dangerous keyword detected: {word}")

    if sender["role"] == "worker" and receiver["role"] == "planner":
        reasons.append("Role violation: worker issuing planner-level command")

    if reasons:
        return {
            "risk_level": "high",
            "reasons": reasons
        }

    return {
        "risk_level": "low",
        "reasons": []
    }
