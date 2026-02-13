# worker.py

def handle_message(message: dict) -> dict:
    print(f"[WORKER] Received task: {message['content']}")
    return {
        "status": "completed",
        "result": "Task executed successfully"
    }
