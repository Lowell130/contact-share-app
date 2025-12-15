from fastapi import APIRouter, Depends, HTTPException, Query
from ..deps import get_current_user, get_current_admin
from ..db import get_db
from ..models import UserOut, CardOut
from typing import List, Optional
from bson import ObjectId
from ..utils import now_utc

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
async def admin_stats(user = Depends(get_current_admin)):
    db = get_db()
    users_count = await db.users.count_documents({})
    cards_count = await db.cards.count_documents({})
    pro_users = await db.users.count_documents({"plan": "pro"})
    
    return {
        "users": users_count,
        "cards": cards_count,
        "pro_users": pro_users
    }

@router.get("/users")
async def list_users(
    skip: int = 0, 
    limit: int = 20, 
    q: Optional[str] = None,
    user = Depends(get_current_admin)
):
    db = get_db()
    filter_q = {}
    if q:
        filter_q = {
            "$or": [
                {"email": {"$regex": q, "$options": "i"}},
                {"name": {"$regex": q, "$options": "i"}}
            ]
        }
        
    cursor = db.users.find(filter_q).skip(skip).limit(limit).sort("created_at", -1)
    users = []
    async for u in cursor:
        users.append({
            "id": str(u["_id"]),
            "email": u["email"],
            "name": u.get("name"),
            "plan": u.get("plan", "free"),
            "created_at": u["created_at"]
        })
    return users

@router.put("/users/{id}")
async def update_user_admin(id: str, payload: dict, user = Depends(get_current_admin)):
    db = get_db()
    try:
        oid = ObjectId(id)
    except:
        raise HTTPException(404, "Invalid ID")
        
    allowed = {k: v for k, v in payload.items() if k in ["plan", "name"]}
    if not allowed:
        return {"ok": False}
        
    await db.users.update_one({"_id": oid}, {"$set": allowed})
    return {"ok": True}

@router.get("/cards")
async def list_all_cards(
    skip: int = 0, 
    limit: int = 20, 
    user = Depends(get_current_admin)
):
    db = get_db()
    cursor = db.cards.find({}).skip(skip).limit(limit).sort("created_at", -1)
    cards = []
    async for c in cursor:
        c["id"] = str(c["_id"])
        c["user_id"] = str(c["user_id"])
        # Fix for some projections if needed, but simple dict is fine
        cards.append(c)
        
    # We might want to return simplified objects or use CardOut but handling ObjectId conversion
    # Let's map to a simple list for basic table
    return cards

@router.get("/settings")
async def get_settings(user = Depends(get_current_admin)):
    db = get_db()
    # Recupera il documento settings (ne esiste solo uno)
    settings = await db.settings.find_one({"_id": "config"})
    if not settings:
        return {}
    # Non ritorniamo tutto se ci sono dati sensibili, ma per l'admin va bene vederli per modificarli
    return {
        "stripe_secret_key": settings.get("stripe_secret_key", ""),
        "stripe_webhook_secret": settings.get("stripe_webhook_secret", ""),
        "stripe_price_id": settings.get("stripe_price_id", "")
    }

@router.put("/settings")
async def update_settings(payload: dict, user = Depends(get_current_admin)):
    db = get_db()
    # Validiamo solo campi noti
    allowed_keys = ["stripe_secret_key", "stripe_webhook_secret", "stripe_price_id"]
    data = {k: v for k, v in payload.items() if k in allowed_keys}
    
    await db.settings.update_one(
        {"_id": "config"}, 
        {"$set": data}, 
        upsert=True
    )
    return {"ok": True}
