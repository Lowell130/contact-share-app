import time, jwt
from passlib.context import CryptContext
from .config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd_ctx.hash(p)

def verify_password(p: str, h: str) -> bool:
    return pwd_ctx.verify(p, h)

def _encode(payload: dict, secret: str, exp_seconds: int):
    now = int(time.time())
    payload = {**payload, "iat": now, "exp": now + exp_seconds}
    return jwt.encode(payload, secret, algorithm="HS256")

def create_access_token(sub: str):
    return _encode({"sub": sub, "typ": "access"}, settings.JWT_SECRET, settings.ACCESS_EXPIRES_MIN * 60)

def create_refresh_token(sub: str, rotation_id: str):
    # rotation_id cambia ad ogni login/refresh per semplice rotation
    return _encode({"sub": sub, "typ": "refresh", "rid": rotation_id}, settings.JWT_REFRESH_SECRET, settings.REFRESH_EXPIRES_DAYS * 24 * 3600)

def decode_access(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

def decode_refresh(token: str):
    return jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"])
