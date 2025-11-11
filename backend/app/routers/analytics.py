from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import timedelta
from ..deps import get_current_user
from ..db import get_db
from ..models import AnalyticsSummary
from ..utils import now_utc

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/cards/{id}/summary", response_model=AnalyticsSummary)
async def summary(id: str, user=Depends(get_current_user)):
    db = get_db()
    card = await db.cards.find_one({"_id": ObjectId(id), "user_id": user["id"]})
    if not card: raise HTTPException(404)
    since = now_utc() - timedelta(days=30)

    total_views = await db.events.count_documents({"card_id": id, "type":"view"})
    total_vcard = await db.events.count_documents({"card_id": id, "type":"vcard_download"})
    pipeline = [
        {"$match": {"card_id": id, "ts": {"$gte": since}}},
        {"$group": {"_id": {"$dateToString": {"format":"%Y-%m-%d","date":"$ts"}}, "count":{"$sum":1}}},
        {"$sort": {"_id": 1}},
    ]
    daily = []
    async for row in db.events.aggregate(pipeline):
        daily.append({"date": row["_id"], "count": row["count"]})
    return AnalyticsSummary(total_views=total_views, total_vcard=total_vcard, last30d=daily)
