from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt


def create_token(payload: Dict[str, Any], secret: str, expires_minutes: int = 30) -> str:
    now = datetime.now(tz=timezone.utc)
    to_encode = {
        **payload,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(to_encode, secret, algorithm="HS256")


def verify_token(token: str, secret: str) -> Dict[str, Any]:
    return jwt.decode(token, secret, algorithms=["HS256"])  # raises jwt exceptions on failure


