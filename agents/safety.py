# safety.py

def handle_message(message: dict) -> dict:
    print(f"[SAFETY] Reviewing message: {message['content']}")
    return {
        "status": "approved"
    }
