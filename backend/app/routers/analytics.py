# app/routers/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import timedelta
from collections import Counter

from ..deps import get_current_user
from ..db import get_db
from ..models import AnalyticsSummary, AnalyticsPoint, AnalyticsReferrer, AnalyticsDevice
from ..utils import now_utc

router = APIRouter(prefix="/analytics", tags=["analytics"])


def categorize_device(ua: str | None) -> str:
    """
    Categoria molto semplice basata sulla user-agent string.
    Puoi raffinarla in seguito.
    """
    if not ua:
        return "other"
    ua_l = ua.lower()
    if "mobile" in ua_l or "android" in ua_l or "iphone" in ua_l:
        return "mobile"
    if "ipad" in ua_l or "tablet" in ua_l:
        return "tablet"
    if "windows" in ua_l or "macintosh" in ua_l or "linux" in ua_l:
        return "desktop"
    return "other"


@router.get("/cards/{id}/summary", response_model=AnalyticsSummary)
async def summary(id: str, user=Depends(get_current_user)):
    db = get_db()

    # Verifica che la card appartenga all'utente loggato
    card = await db.cards.find_one({"_id": ObjectId(id), "user_id": user["id"]})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    now = now_utc()
    since_24h = now - timedelta(hours=24)
    since_7d = now - timedelta(days=7)
    since_30d = now - timedelta(days=30)

    # --- Totali ---
    total_views = await db.events.count_documents({"card_id": id, "type": "view"})
    total_vcard = await db.events.count_documents({"card_id": id, "type": "vcard_download"})

    # --- Views ultime 24h / 7 giorni ---
    views_24h = await db.events.count_documents({
        "card_id": id,
        "type": "view",
        "ts": {"$gte": since_24h},
    })
    views_7d = await db.events.count_documents({
        "card_id": id,
        "type": "view",
        "ts": {"$gte": since_7d},
    })

    # --- Serie giornaliera ultimi 30 giorni ---
    pipeline_daily = [
        {
            "$match": {
                "card_id": id,
                "type": "view",
                "ts": {"$gte": since_30d},
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$ts",
                    }
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    daily: list[AnalyticsPoint] = []
    async for row in db.events.aggregate(pipeline_daily):
        daily.append(AnalyticsPoint(date=row["_id"], count=row["count"]))

    # --- Referrer (ultimi 30 giorni, solo view) ---
    ref_counter: Counter[str] = Counter()
    dev_counter: Counter[str] = Counter()

    cursor = db.events.find(
        {
            "card_id": id,
            "type": "view",
            "ts": {"$gte": since_30d},
        },
        {"ref": 1, "ua": 1, "_id": 0},
    )

    async for ev in cursor:
        ref = ev.get("ref") or "direct"
        ref_counter[ref] += 1

        ua = ev.get("ua")
        dev = categorize_device(ua)
        dev_counter[dev] += 1

    top_referrers = [
        AnalyticsReferrer(ref=ref, count=count)
        for ref, count in ref_counter.most_common(5)
    ]

    devices = [
        AnalyticsDevice(kind=kind, count=count)
        for kind, count in dev_counter.items()
    ]

    return AnalyticsSummary(
        total_views=total_views,
        total_vcard=total_vcard,
        views_24h=views_24h,
        views_7d=views_7d,
        last30d=daily,
        top_referrers=top_referrers,
        devices=devices,
    )
