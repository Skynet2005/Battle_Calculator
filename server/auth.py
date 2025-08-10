from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_secret() -> str:
    secret = os.getenv("JWT_SECRET", "change-this-secret")
    return secret


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        return False


def create_access_token(user_id: int, username: str, expires_minutes: int = 7 * 24 * 60) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
        "type": "access",
    }
    token = jwt.encode(payload, get_secret(), algorithm="HS256")
    return token


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, get_secret(), algorithms=["HS256"])
    except Exception:
        return None


