"""
In-memory store for pending business registrations (OTP + payload).
Key: business email (lowercase). Value: { otp, payload, expires_at }.
TTL 10 minutes. For production consider Redis.
"""
import time
from typing import Any

PENDING_TTL_SECONDS = 600  # 10 minutes

_pending: dict[str, dict[str, Any]] = {}


def set_pending(email: str, otp: str, payload: dict[str, Any]) -> None:
    key = email.strip().lower()
    _pending[key] = {
        "otp": otp,
        "payload": payload,
        "expires_at": time.time() + PENDING_TTL_SECONDS,
    }


def get_pending(email: str) -> dict[str, Any] | None:
    key = email.strip().lower()
    entry = _pending.get(key)
    if not entry:
        return None
    if time.time() > entry["expires_at"]:
        del _pending[key]
        return None
    return entry


def pop_pending(email: str) -> dict[str, Any] | None:
    key = email.strip().lower()
    entry = _pending.pop(key, None)
    if not entry or time.time() > entry["expires_at"]:
        return None
    return entry
