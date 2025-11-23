# app/routers/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import timedelta
from ..deps import get_current_user
from ..db import get_db
from ..utils import now_utc

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/cards/{id}/summary")
async def summary(id: str, user=Depends(get_current_user)):
    """
    Ritorna:
    {
      total_views: int,
      total_vcard: int,
      views_24h: int,
      views_7d: int,
      last30d: [{date: 'YYYY-MM-DD', count: int}],
      top_referrers: [{ref: str, count: int}],
      devices: [{kind: 'desktop'|'mobile'|'tablet'|'unknown', count: int}],
      social_clicks: [{social: str, count: int}],
      top_countries: [{country: str, count: int}]
    }
    """
    db = get_db()

    # Verifica che la card appartenga all'utente
    card = await db.cards.find_one({"_id": ObjectId(id), "user_id": user["id"]})
    if not card:
        raise HTTPException(404)

    now = now_utc()
    since_30d = now - timedelta(days=30)
    since_24h = now - timedelta(hours=24)
    since_7d = now - timedelta(days=7)

    # --- KPI base ---
    total_views = await db.events.count_documents({"card_id": id, "type": "view"})
    total_vcard = await db.events.count_documents({"card_id": id, "type": "vcard_download"})
    views_24h = await db.events.count_documents(
        {"card_id": id, "type": "view", "ts": {"$gte": since_24h}}
    )
    views_7d = await db.events.count_documents(
        {"card_id": id, "type": "view", "ts": {"$gte": since_7d}}
    )

    # --- Andamento ultimi 30 giorni (solo view) ---
    daily = []
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
    async for row in db.events.aggregate(pipeline_daily):
        daily.append({"date": row["_id"], "count": row["count"]})

    # --- Top referrer ultimi 30 giorni ---
    top_referrers = []
    pipeline_ref = [
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
                    "$ifNull": ["$ref", "direct"]
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    async for row in db.events.aggregate(pipeline_ref):
        top_referrers.append({
            "ref": row["_id"],
            "count": row["count"],
        })

    # --- Device breakdown (via user-agent, come avevi) ---
    devices = []
    pipeline_dev = [
        {
            "$match": {
                "card_id": id,
                "type": "view",
                "ts": {"$gte": since_30d},
            }
        },
        {
            "$group": {
                "_id": "$ua",
                "count": {"$sum": 1},
            }
        },
    ]

    import re

    def classify_ua(ua: str) -> str:
        if not ua:
            return "unknown"
        s = ua.lower()
        if "mobile" in s or "android" in s or "iphone" in s:
            return "mobile"
        if "ipad" in s or "tablet" in s:
            return "tablet"
        if re.search(r"windows|macintosh|linux", s):
            return "desktop"
        return "unknown"

    tmp_dev = {}
    async for row in db.events.aggregate(pipeline_dev):
        ua = row["_id"]
        cnt = row["count"]
        kind = classify_ua(ua or "")
        tmp_dev[kind] = tmp_dev.get(kind, 0) + cnt

    for k, v in tmp_dev.items():
        devices.append({"kind": k, "count": v})

    # --- Social clicks ultimi 30 giorni ---
    social_clicks = []
    pipeline_social = [
        {
            "$match": {
                "card_id": id,
                "type": "social_click",
                "ts": {"$gte": since_30d},
            }
        },
        {
            "$group": {
                # Prima "social", poi "social_type", poi "unknown"
                "_id": {
                    "$ifNull": [
                        "$social",
                        {
                            "$ifNull": ["$social_type", "unknown"]
                        }
                    ]
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
    ]
    async for row in db.events.aggregate(pipeline_social):
        social_clicks.append({
            "social": row["_id"],
            "count": row["count"],
        })

    # --- 🌍 Geo analytics: top paesi ultimi 30 giorni ---
    top_countries = []
    pipeline_geo = [
    {
        "$match": {
            "card_id": id,
            "ts": {"$gte": since_30d},
        }
    },
    {
        "$group": {
            "_id": {
                "$ifNull": ["$country", "unknown"]
            },
            "count": {"$sum": 1},
        }
    },
    {"$sort": {"count": -1}},
    {"$limit": 10},
]

    
    async for row in db.events.aggregate(pipeline_geo):
        if row["_id"] == "unknown":
            continue  # 👈 nasconde gli unknown dal grafico
        top_countries.append({
            "country": row["_id"],
            "count": row["count"],
        })

    return {
        "total_views": total_views,
        "total_vcard": total_vcard,
        "views_24h": views_24h,
        "views_7d": views_7d,
        "last30d": daily,
        "top_referrers": top_referrers,
        "devices": devices,
        "social_clicks": social_clicks,
        "top_countries": top_countries,   # 👈 usato dal frontend per il grafico geo
    }
