# app/routers/public.py
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import JSONResponse, Response
from ..db import get_db
from ..utils import now_utc
from ..services.vcard import to_vcard

import httpx  # 👈 nuovo import

router = APIRouter(prefix="/public", tags=["public"])


async def detect_country(request: Request) -> str:
    """
    1. Prova a leggere header geo (se in futuro metti un proxy/CDN che li aggiunge)
    2. Se non ci sono, usa l'IP da X-Forwarded-For e fa geo-IP con ipapi.co
    """
    # 1) Header "classici" se un giorno ci metti davanti Vercel/Cloudflare/LB custom
    for h in (
        "cf-ipcountry",
        "x-vercel-ip-country",
        "x-country",
        "x-geo-country",
        "x-appengine-country",  # per compat App Engine/LB
        "x-user-country",
    ):
        v = request.headers.get(h)
        if v:
            return v.strip().upper()

    # 2) Recupera l'IP reale (primo IP della catena X-Forwarded-For)
    xff = request.headers.get("x-forwarded-for")
    ip = None
    if xff:
        ip = xff.split(",")[0].strip()
    elif request.client:
        ip = request.client.host

    # IP locali / privati -> niente geoloc
    if not ip or ip.startswith(("127.", "10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
                                "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
                                "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.")):
        return "unknown"

    # 3) Geo-IP via ipapi.co (free con qualche limite, ma per ora va benissimo)
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(f"https://ipapi.co/{ip}/country/")
            if r.status_code == 200:
                code = (r.text or "").strip().upper()
                if code and len(code) == 2:
                    return code
    except Exception:
        # in caso di errori (timeout, ecc.) non blocchiamo la view
        pass

    return "unknown"


@router.get("/cards/{slug}")
async def public_card(slug: str, request: Request):
    db = get_db()
    c = await db.cards.find_one({"slug": slug})
    if not c or not c.get("is_public", True):
        raise HTTPException(404)

    # track view
    await db.events.insert_one({
        "card_id": str(c["_id"]),
        "type": "view",
        "ua": request.headers.get("user-agent"),
        "ref": request.headers.get("referer"),
        "country": await detect_country(request),  # 👈 ora è async
        "ts": now_utc(),
    })

    c["id"] = str(c["_id"])
    c["user_id"] = str(c["user_id"])

    return {
        "id": c["id"],
        "slug": c["slug"],
        "title": c.get("title"),
        "notes": c.get("notes", ""),
        "fields": c.get("fields", []),
        "theme": c.get("theme"),
        "avatar_url": c.get("avatar_url"),
        "is_indexed": c.get("is_indexed", True),
        "allow_vcard": c.get("allow_vcard", True),
        "cta": "Salva in rubrica",
    }


@router.get("/cards/{slug}/vcard")
async def public_vcard(slug: str, request: Request):
    db = get_db()
    c = await db.cards.find_one({"slug": slug})
    if not c or not c.get("is_public", True) or not c.get("allow_vcard", True):
        raise HTTPException(404)

    await db.events.insert_one({
        "card_id": str(c["_id"]),
        "type": "vcard_download",
        "ua": request.headers.get("user-agent"),
        "ref": request.headers.get("referer"),
        "country": await detect_country(request),  # 👈 idem
        "ts": now_utc(),
    })

    vcf = to_vcard(c.get("title") or "Contact", c.get("fields", []))
    headers = {"Content-Disposition": f'attachment; filename="{c["slug"]}.vcf"'}

    return Response(content=vcf, media_type="text/vcard", headers=headers)


@router.post("/events/social-click")
async def public_social_click(
    request: Request,
    payload: dict = Body(...),
):
    """
    Traccia un click su un link social di una card pubblica.

    Body atteso:
    {
      "card_id": "...",
      "social_type": "instagram" | "linkedin" | ...,
      "target": "https://instagram.com/..."
    }
    """
    db = get_db()

    card_id = payload.get("card_id")
    social_type = (payload.get("social_type") or "").lower()
    target = payload.get("target")

    if not card_id or not social_type:
        raise HTTPException(status_code=400, detail="card_id and social_type are required")

    await db.events.insert_one({
        "card_id": card_id,
        "type": "social_click",
        "social_type": social_type,
        "target": target,
        "ua": request.headers.get("user-agent"),
        "ref": request.headers.get("referer"),
        "country": await detect_country(request),  # 👈 anche qui
        "ts": now_utc(),
    })

    return {"ok": True}
