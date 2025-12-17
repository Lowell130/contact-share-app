from fastapi import APIRouter, Depends, HTTPException, Query
from ..deps import get_current_user, get_current_admin
from ..db import get_db
from ..models import UserOut, CardOut
from typing import List, Optional
from bson import ObjectId
from ..utils import now_utc
from datetime import timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
async def admin_stats(user = Depends(get_current_admin)):
    db = get_db()
    users_count = await db.users.count_documents({})
    cards_count = await db.cards.count_documents({})
    pro_users_count = await db.users.count_documents({"plan": "pro"})
    
    # Recent users
    recent_users = []
    async for u in db.users.find({}).sort("created_at", -1).limit(5):
        recent_users.append({
            "email": u["email"],
            "name": u.get("name"),
            "plan": u.get("plan", "free"),
            "created_at": u["created_at"]
        })

    # Recent PRO users (approximate based on creation date or we filter by plan)
    # Ideally we'd have a 'plan_updated_at' but 'created_at' + filter is okay for now if they signed up as pro or upgraded recently 
    # (Note: this just shows NEW users who are PRO, not necessarily upgraded existing users unless we track upgrades separately)
    recent_pro = []
    async for u in db.users.find({"plan": "pro"}).sort("created_at", -1).limit(5):
        recent_pro.append({
            "email": u["email"],
            "name": u.get("name"),
            "plan": u.get("plan", "pro"),
            "created_at": u["created_at"]
        })

    return {
        "users": users_count,
        "cards": cards_count,
        "pro_users": pro_users_count,
        "recent_users": recent_users,
        "recent_pro_users": recent_pro
    }

@router.get("/analytics/global")
async def admin_analytics(user = Depends(get_current_admin)):
    db = get_db()
    now = now_utc()
    since_30d = now - timedelta(days=30)
    
    # --- Top Countries (Global) ---
    top_countries = []
    pipeline_geo = [
        { "$match": { "ts": {"$gte": since_30d} } },
        { "$group": { "_id": { "$ifNull": ["$country", "unknown"] }, "count": {"$sum": 1} } },
        { "$sort": { "count": -1 } },
        { "$limit": 10 },
    ]
    async for row in db.events.aggregate(pipeline_geo):
        if row["_id"] == "unknown": continue
        top_countries.append({ "country": row["_id"], "count": row["count"] })

    # --- Top Referrers (Global) ---
    top_referrers = []
    pipeline_ref = [
        { "$match": { "type": "view", "ts": {"$gte": since_30d} } },
        { "$group": { "_id": { "$ifNull": ["$ref", "direct"] }, "count": {"$sum": 1} } },
        { "$sort": { "count": -1 } },
        { "$limit": 10 },
    ]
    async for row in db.events.aggregate(pipeline_ref):
        top_referrers.append({ "ref": row["_id"], "count": row["count"] })

    # --- Views Last 30 Days (Global) ---
    daily_views = []
    pipeline_daily = [
        { "$match": { "type": "view", "ts": {"$gte": since_30d} } },
        {
            "$group": {
                "_id": { "$dateToString": { "format": "%Y-%m-%d", "date": "$ts" } },
                "count": {"$sum": 1},
            }
        },
        { "$sort": { "_id": 1 } },
    ]
    async for row in db.events.aggregate(pipeline_daily):
        daily_views.append({ "date": row["_id"], "count": row["count"] })

    return {
        "top_countries": top_countries,
        "top_referrers": top_referrers,
        "last30d": daily_views
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
        if "user_id" in c:
            c["user_id"] = str(c["user_id"])
        
        # Remove original ObjectId to avoid serialization error
        c.pop("_id", None)
        
        cards.append(c)
        
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
