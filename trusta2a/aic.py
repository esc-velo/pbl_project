# aic.py
# Agent Identity Certificate (AIC)

import hmac
import hashlib


def sign_message(secret_key: str, message_payload: str) -> str:
    return hmac.new(
        secret_key.encode(),
        message_payload.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_signature(secret_key: str, message_payload: str, signature: str) -> bool:
    expected = sign_message(secret_key, message_payload)
    return hmac.compare_digest(expected, signature)
