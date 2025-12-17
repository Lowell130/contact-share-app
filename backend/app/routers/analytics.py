# app/routers/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import timedelta
from ..deps import get_current_user
from ..db import get_db
from ..utils import now_utc

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/cards/{id}/summary")
async def summary(id: str, days: int = 30, user=Depends(get_current_user)):
    """
    Ritorna:
    {
      total_views: int,
      total_vcard: int,
      views_24h: int,
      views_7d: int,
      last30d: [{date: 'YYYY-MM-DD', count: int}],  # renamed conceptually to 'history' in frontend if needed, but keeping key for compat
      top_referrers: [{ref: str, count: int}],
      devices: [{kind: 'desktop'|'mobile'|'tablet'|'unknown', count: int}],
      os_breakdown: [{os: str, count: int}],
      social_clicks: [{social: str, count: int}],
      top_countries: [{country: str, count: int}]
    }
    """
    db = get_db()

    # Verifica card
    card = await db.cards.find_one({"_id": ObjectId(id), "user_id": user["id"]})
    if not card:
        raise HTTPException(404)

    now = now_utc()
    since_period = now - timedelta(days=days)
    since_24h = now - timedelta(hours=24)
    since_7d = now - timedelta(days=7)

    # --- KPI base (Always total) ---
    total_views = await db.events.count_documents({"card_id": id, "type": "view"})
    total_vcard = await db.events.count_documents({"card_id": id, "type": "vcard_download"})
    
    # Recent metrics (fixed windows)
    views_24h = await db.events.count_documents(
        {"card_id": id, "type": "view", "ts": {"$gte": since_24h}}
    )
    views_7d = await db.events.count_documents(
        {"card_id": id, "type": "view", "ts": {"$gte": since_7d}}
    )

    # --- History (Filtered by days) ---
    daily = []
    pipeline_daily = [
        {
            "$match": {
                "card_id": id,
                "type": "view",
                "ts": {"$gte": since_period},
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

    # --- Top referrer (Filtered) ---
    top_referrers = []
    pipeline_ref = [
        {
            "$match": {
                "card_id": id,
                "type": "view",
                "ts": {"$gte": since_period},
            }
        },
        {
            "$group": {
                "_id": { "$ifNull": ["$ref", "direct"] },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    async for row in db.events.aggregate(pipeline_ref):
        top_referrers.append({ "ref": row["_id"], "count": row["count"] })

    # --- Device & OS (Filtered) ---
    devices = []
    os_stats = []
    
    pipeline_ua = [
        {
            "$match": {
                "card_id": id,
                "type": "view",
                "ts": {"$gte": since_period},
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

    def classify_ua(ua: str):
        if not ua: return "unknown", "Unknown"
        s = ua.lower()
        
        # Device
        device = "unknown"
        if "mobile" in s or "android" in s or "iphone" in s: device = "mobile"
        elif "ipad" in s or "tablet" in s: device = "tablet"
        elif re.search(r"windows|macintosh|linux", s): device = "desktop"
        
        # OS
        os_name = "Other"
        if "windows" in s: os_name = "Windows"
        elif "iphone" in s or "ipad" in s: os_name = "iOS"
        elif "macintosh" in s or "mac os" in s: os_name = "macOS"
        elif "android" in s: os_name = "Android"
        elif "linux" in s: os_name = "Linux"
        
        return device, os_name

    tmp_dev = {}
    tmp_os = {}
    
    async for row in db.events.aggregate(pipeline_ua):
        ua_str = row["_id"] or ""
        cnt = row["count"]
        d_kind, os_kind = classify_ua(ua_str)
        
        tmp_dev[d_kind] = tmp_dev.get(d_kind, 0) + cnt
        tmp_os[os_kind] = tmp_os.get(os_kind, 0) + cnt

    for k, v in tmp_dev.items():
        devices.append({"kind": k, "count": v})
    
    for k, v in tmp_os.items():
        os_stats.append({"os": k, "count": v})

    # --- Social clicks (Filtered) ---
    social_clicks = []
    pipeline_social = [
        {
            "$match": {
                "card_id": id,
                "type": "social_click",
                "ts": {"$gte": since_period},
            }
        },
        {
            "$group": {
                "_id": { "$ifNull": ["$social", { "$ifNull": ["$social_type", "unknown"] }] },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
    ]
    async for row in db.events.aggregate(pipeline_social):
        social_clicks.append({ "social": row["_id"], "count": row["count"] })

    # --- Geo analytics (Filtered) ---
    top_countries = []
    pipeline_geo = [
        {
            "$match": {
                "card_id": id,
                "ts": {"$gte": since_period},
            }
        },
        {
            "$group": {
                "_id": { "$ifNull": ["$country", "unknown"] },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]

    async for row in db.events.aggregate(pipeline_geo):
        if row["_id"] == "unknown": continue
        top_countries.append({ "country": row["_id"], "count": row["count"] })

    return {
        "total_views": total_views,
        "total_vcard": total_vcard,
        "views_24h": views_24h,
        "views_7d": views_7d,
        "last30d": daily, # Keeping key for frontend compat, but represents 'filtered period'
        "top_referrers": top_referrers,
        "devices": devices,
        "os_breakdown": os_stats,
        "social_clicks": social_clicks,
        "top_countries": top_countries,
    }

@router.get("/cards/{id}/export")
async def export_analytics(id: str, days: int = 30, user=Depends(get_current_user)):
    # Simple CSV export
    db = get_db()
    card = await db.cards.find_one({"_id": ObjectId(id), "user_id": user["id"]})
    if not card: raise HTTPException(404)
    
    # We will export Daily Views for the selected period
    now = now_utc()
    since_period = now - timedelta(days=days)
    
    pipeline = [
        { "$match": { "card_id": id, "type": "view", "ts": {"$gte": since_period} } },
        { "$project": { "ts": 1, "country": 1, "ref": 1, "ua": 1 } },
        { "$sort": { "ts": -1 } }
    ]
    
    import csv
    import io
    from fastapi.responses import StreamingResponse
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp (UTC)", "Type", "Country", "Referrer", "User-Agent"])
    
    async for row in db.events.aggregate(pipeline):
        writer.writerow([
            row.get("ts", "").isoformat(),
            "view",
            row.get("country", "unknown"),
            row.get("ref", "direct"),
            row.get("ua", "")
        ])
        
    output.seek(0)
    
    headers = {
        "Content-Disposition": f'attachment; filename="analytics_{card.get("slug", id)}_{days}d.csv"'
    }
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)

