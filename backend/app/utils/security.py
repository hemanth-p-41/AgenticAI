from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt (direct `bcrypt` library).

    bcrypt has a 72-byte limitation; we truncate deterministically.
    Returns UTF-8 decoded hash for storage.
    """
    if isinstance(password, str):
        raw = password.encode('utf-8')
    else:
        raw = bytes(password)
    if len(raw) > 72:
        raw = raw[:72]
    hashed = bcrypt.hashpw(raw, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against stored bcrypt hash."""
    if isinstance(plain_password, str):
        raw = plain_password.encode('utf-8')
    else:
        raw = bytes(plain_password)
    if len(raw) > 72:
        raw = raw[:72]
    try:
        return bcrypt.checkpw(raw, hashed_password.encode('utf-8'))
    except Exception:
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token containing `data` payload.

    Args:
        data: payload data (e.g., {'user_id': 1})
        expires_delta: optional timedelta for expiration
    Returns:
        JWT as string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT. Raises JWTError on failure."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise
