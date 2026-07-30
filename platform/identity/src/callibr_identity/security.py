from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from callibr_kernel import CallibrError


class AuthenticationFailedError(CallibrError):
    def __init__(self) -> None:
        super().__init__(
            "AUTHENTICATION_FAILED",
            "Invalid credentials.",
        )


class InvalidTokenError(CallibrError):
    def __init__(self, reason: str = "invalid token") -> None:
        super().__init__(
            "AUTH_TOKEN_INVALID",
            "Authentication token is invalid.",
            details={"reason": reason},
        )


def hash_password(password: str, *, salt: str | None = None) -> str:
    password_salt = salt or secrets.token_urlsafe(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        password_salt.encode("utf-8"),
        210_000,
    ).hex()
    return f"pbkdf2_sha256${password_salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, salt, expected_digest = stored_hash.split("$", 2)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    candidate = hash_password(password, salt=salt).split("$", 2)[2]
    return hmac.compare_digest(candidate, expected_digest)


def encode_token(claims: dict[str, Any], *, secret: str, ttl_seconds: int) -> str:
    now = datetime.now(tz=UTC)
    payload = {
        **claims,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp()),
    }
    header_segment = _base64url_encode({"alg": "HS256", "typ": "JWT"})
    payload_segment = _base64url_encode(payload)
    signature = _sign(f"{header_segment}.{payload_segment}", secret)
    return f"{header_segment}.{payload_segment}.{signature}"


def decode_token(token: str, *, secret: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidTokenError("malformed token")
    header_segment, payload_segment, signature = parts
    expected_signature = _sign(f"{header_segment}.{payload_segment}", secret)
    if not hmac.compare_digest(signature, expected_signature):
        raise InvalidTokenError("bad signature")

    payload = _base64url_decode(payload_segment)
    expires_at = payload.get("exp")
    if not isinstance(expires_at, int):
        raise InvalidTokenError("missing expiration")
    if expires_at < int(datetime.now(tz=UTC).timestamp()):
        raise InvalidTokenError("expired token")
    return payload


def _sign(value: str, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def _base64url_encode(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return base64.urlsafe_b64encode(encoded).decode("ascii").rstrip("=")


def _base64url_decode(value: str) -> dict[str, Any]:
    try:
        padded = value + "=" * (-len(value) % 4)
        decoded = base64.urlsafe_b64decode(padded.encode("ascii"))
        payload = json.loads(decoded.decode("utf-8"))
    except (ValueError, json.JSONDecodeError) as exc:
        raise InvalidTokenError("bad payload") from exc
    if not isinstance(payload, dict):
        raise InvalidTokenError("bad payload")
    return payload
