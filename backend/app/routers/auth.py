# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends, status, Body
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from bson import ObjectId
from datetime import timedelta, timezone
import logging
import secrets
from ..db import get_db
from ..models import UserIn, LoginIn, TokenPair, MagicRequestIn, MagicConfirmIn
from ..security import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh
from ..utils import now_utc
from ..deps import get_current_user

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

from ..models import ForgotPasswordIn, ResetPasswordIn
from ..email import send_email
from ..config import settings

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordIn):
    db = get_db()
    user = await db.users.find_one({"email": data.email})
    if not user:
        # Avoid user enumeration: returning OK even if email not found
        return {"ok": True, "msg": "If the email exists, a reset link has been sent."}
    
    # Generate token
    token = secrets.token_urlsafe(32)
    await db.reset_tokens.insert_one({
        "token": token,
        "user_id": str(user["_id"]),
        "created_at": now_utc(),
        "expires_at": now_utc() + timedelta(minutes=30)
    })
    
    link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    html = f"""
    <h3>Password Reset</h3>
    <p>We received a request to reset your password.</p>
    <p>Click the link below to set a new password:</p>
    <a href="{link}">Reset Password</a>
    <p>This link expires in 30 minutes.</p>
    """
    
    await send_email(data.email, "Reset Password - Contact Share", html)
    return {"ok": True, "msg": "Reset link sent."}

@router.post("/reset-password")
async def reset_password(data: ResetPasswordIn):
    logger = logging.getLogger("uvicorn.error")
    try:
        db = get_db()
        
        # Validate token
        t = await db.reset_tokens.find_one({"token": data.token})
        now = now_utc()
        
        if not t:
            raise HTTPException(400, "Invalid token")
        
        # FIX: Ensure timezone awareness
        expires_at = t["expires_at"]
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < now:
            await db.reset_tokens.delete_one({"_id": t["_id"]})
            raise HTTPException(400, "Token expired")
        
        uid = t["user_id"]
        new_hash = hash_password(data.new_password)
        
        await db.users.update_one(
            {"_id": ObjectId(uid)},
            {"$set": {"password_hash": new_hash}}
        )
        
        # Consuma il token
        await db.reset_tokens.delete_one({"_id": t["_id"]})
        
        return {"ok": True, "msg": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password: {e}", exc_info=True)
        # Re-raise as 500 so client sees error, but logs contain detail
        raise HTTPException(status_code=500, detail="Internal Server Error during password reset")

@router.delete("/me")
async def delete_account(user=Depends(get_current_user)):
    db = get_db()
    uid = user["id"]
    oid = ObjectId(uid)
    
    # Delete all cards
    await db.cards.delete_many({"user_id": oid})
    
    # Delete user
    await db.users.delete_one({"_id": oid})
    
    return {"ok": True}
