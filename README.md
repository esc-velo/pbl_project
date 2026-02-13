# TRUSTA2A  
**Trust-Scored Agent-to-Agent Communication Protocol (v1 Prototype)**

---

## 1. Problem and Goal

Modern multi-agent LLM systems (planners, workers, critics, tool agents, etc.) typically assume that **all internal agents are trustworthy by default**. This assumption introduces serious systemic risks:

### Core Gaps

1. **No identity verification**
   - Any component capable of sending a message can impersonate another agent.
   - There is no cryptographic or protocol-level guarantee of who actually sent a message.

2. **No behavioral memory or reputation**
   - Agents are not judged by their past behavior.
   - A repeatedly unsafe or misconfigured agent is treated the same as a consistently safe one.

3. **No pre-execution risk control**
   - Messages are often executed immediately once generated.
   - There is no centralized checkpoint asking whether a message is safe, allowed, or within the sender’s role.

In complex systems, a single compromised or faulty agent can cause **cascading failures**, with harmful outputs propagating across the agent graph.

### Goal of TRUSTA2A

TRUSTA2A introduces a **governed agent-to-agent (A2A) communication protocol** that forces *every* inter-agent message through a mandatory security layer that:

1. Verifies the sender’s identity (**Agent Identity Certificate – AIC**)
2. Tracks and evaluates the sender’s reputation (**Dynamic Trust Score – DTS**)
3. Assesses message risk before execution (**Behavioral Risk Assessment – BRA**)

---

## 2. High-Level Architecture

### Core Idea

Insert a **TRUSTA2A Router** as a mandatory intermediary so that:

> **No agent ever directly communicates with another agent.**

All agent-to-agent messages must pass through the router.

### Conceptual Data Flow

```Agent A → TRUSTA2A Router (AIC + DTS + BRA) → Agent B```


### Router Responsibilities

For every message, the router:
1. Verifies identity (AIC)
2. Checks and updates trust score (DTS)
3. Evaluates message risk (BRA)
4. Decides whether to forward, block, or quarantine
5. Logs all decisions

This makes TRUSTA2A **non-optional** and **protocol-enforced**.

---

## 3. Core Data Structures

### 3.1 Agent Registry and Identity (AIC)

Each agent is registered with static identity data:

```python
Agent = {
    "agent_id": str,
    "role": str,
    "trust_score": float,
    "status": str
}
```

A global registry:

```python
AGENTS = {
    "planner": {...},
    "worker": {...},
    "safety": {...}
}
```

Each agent also has a secret key (prototype HMAC):

```python
AGENT_SECRETS = {
    "planner": "secret_planner_key",
    "worker": "secret_worker_key",
    "safety": "secret_safety_key"
}
```

The Agent Identity Certificate (AIC) is effectively the trusted tuple:
(agent_id, role, secret/public key) maintained by the router.

### 3.2 Message Format

All agent-to-agent messages must use a single canonical structure:

```python
Message = {
    "sender_id": str,
    "receiver_id": str,
    "content": str,
    "timestamp": float,
    "intent": str,
    "risk_metadata": dict,
    "signature": str
}
```

## 4. Pillar 1 – Agent Identity Certificate (AIC)

**Objective:** Prevent spoofing and impersonation.

### How It Works (Prototype)

- Each agent signs messages using an **HMAC-SHA256** secret.
- The TRUSTA2A Router recomputes and verifies the signature.
- Signature mismatch or unknown sender ⇒ **message is blocked**.

### Effects

- Spoofed messages are rejected at the protocol layer.
- Serious identity violations strongly degrade trust.

---

## 5. Pillar 2 – Dynamic Trust Score (DTS)

**Objective:** Maintain a continuously evolving reputation for each agent.

### Trust Score

- Range: **[0.0, 1.0]** (prototype)
- Higher = more reliable
- Lower = riskier

### Update Rules (v1)

| Event                          | Trust Change |
|--------------------------------|--------------|
| Safe action                    | +0.05        |
| High-risk message blocked      | −0.20        |
| Serious violation (spoofing)   | −0.50        |

Trust values are clamped to **[0.0, 1.0]**.

### Quarantine Policy
Quarantined agents are blocked from sending any further messages.

```python
if trust < 0.1:
    agent.status = "quarantined"
```

## 6. Pillar 3 – Behavioral Risk Assessment (BRA)

**Objective:** Assess message risk **before execution**.

### Inputs

- Message content  
- Sender role  
- Receiver role  

### Prototype Rules

- Dangerous keywords (e.g. `rm -rf`, `delete`, `disable safety`) ⇒ **high risk**
- Role violations ⇒ **high risk**
- Otherwise ⇒ **low risk**

### Router Behavior

- **Low risk** → message forwarded
- **High risk** → message blocked + trust penalty

BRA prevents blind execution of dangerous instructions.

---

## 7. TRUSTA2A Router Algorithm

For each incoming message:

### 1. Identity Check (AIC)

- Verify sender exists  
- Verify signature  
- Block on failure  

### 2. Trust Check (DTS)

- Block quarantined agents  

### 3. Risk Assessment (BRA)

- Evaluate content and roles  
- Block high-risk messages  

### 4. Forwarding

- Dispatch message to receiver agent handler  

### 5. Post-Execution Update

- Update trust score based on outcome  

### 6. Logging

- Print all decisions for auditability  

The router is the **only allowed path** for agent communication.

---

## 8. Demo Scenarios (`demo.py`)

The included demo demonstrates:

- Normal planner → worker flow  
- High-risk message blocked  
- Spoofed message blocked  
- Trust score degradation  
- Automatic agent quarantine  

Run:

```bash
python demo.py
```

## 9. Why the Router Is Mandatory

Without a mandatory router:

- Identity is unverifiable  
- Trust cannot accumulate  
- Risk checks are optional and inconsistent  

With TRUSTA2A:

- Identity, trust, and risk become **first-class protocol concepts**
- Unsafe agents are automatically constrained
- Failures are localized instead of cascading

---

## 10. Scope and Future Extensions

This v1 prototype intentionally prioritizes:

- Correctness  
- Clarity  
- Modularity  

Future versions can add:

- Public-key cryptography  
- Trust decay and time-based models  
- Safety-agent escalation paths  
- Human-in-the-loop approvals  
- Integration with real LLM orchestration frameworks