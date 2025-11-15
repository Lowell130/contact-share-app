# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends, status, Body
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from bson import ObjectId
from datetime import timedelta
import secrets
from ..db import get_db
from ..models import UserIn, LoginIn, TokenPair, MagicRequestIn, MagicConfirmIn
from ..security import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh
from ..utils import now_utc

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenPair)
async def register(data: UserIn):
    db = get_db()
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    doc = {
        "email": data.email,
        "password_hash": hash_password(data.password) if data.password else None,
        "name": data.name or data.email.split("@")[0],
        "plan": "free",
        "created_at": now_utc(),
    }
    res = await db.users.insert_one(doc)
    uid = str(res.inserted_id)
    rid = secrets.token_hex(8)
    return TokenPair(access_token=create_access_token(uid), refresh_token=create_refresh_token(uid, rid))

@router.post("/login", response_model=TokenPair)
async def login(data: LoginIn):
    db = get_db()
    user = await db.users.find_one({"email": data.email})
    if not user or not user.get("password_hash") or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    uid = str(user["_id"])
    rid = secrets.token_hex(8)
    return TokenPair(access_token=create_access_token(uid), refresh_token=create_refresh_token(uid, rid))

@router.post("/refresh", response_model=TokenPair)
async def refresh(token: str = Body(..., embed=True)):
    try:
        payload = decode_refresh(token)
        uid = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    rid = secrets.token_hex(8)  # semplice rotation
    return TokenPair(access_token=create_access_token(uid), refresh_token=create_refresh_token(uid, rid))

# MAGIC LINK (dev-friendly: ritorna il token in risposta per test)
@router.post("/magic/request")
async def magic_request(data: MagicRequestIn):
    db = get_db()
    user = await db.users.find_one({"email": data.email})
    if not user:
        # autocrea free account senza password
        doc = {
            "email": data.email,
            "password_hash": None,
            "name": data.email.split("@")[0],
            "plan": "free",
            "created_at": now_utc(),
        }
        r = await db.users.insert_one(doc)
        user_id = str(r.inserted_id)
    else:
        user_id = str(user["_id"])
    token = secrets.token_urlsafe(32)
    await db.magic_tokens.insert_one({
        "token": token,
        "user_id": user_id,
        "created_at": now_utc(),
        "expires_at": now_utc() + timedelta(minutes=15),
    })
    # In produzione invia email; qui lo ritorniamo per test
    return {"ok": True, "token": token}

@router.post("/magic/confirm", response_model=TokenPair)
async def magic_confirm(data: MagicConfirmIn):
    db = get_db()
    t = await db.magic_tokens.find_one({"token": data.token})
    if not t:
        raise HTTPException(status_code=400, detail="Invalid magic token")
    uid = t["user_id"]
    await db.magic_tokens.delete_one({"_id": t["_id"]})
    rid = secrets.token_hex(8)
    return TokenPair(access_token=create_access_token(uid), refresh_token=create_refresh_token(uid, rid))
