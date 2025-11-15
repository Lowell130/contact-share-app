# app/routers/public.py
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import Response
from ..db import get_db
from ..utils import now_utc
from ..services.vcard import to_vcard

# ✅ Prefisso /public per separare chiaramente le route pubbliche da /cards/{id}
router = APIRouter(prefix="/public", tags=["public"])


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
        "ts": now_utc(),
    })

    return {"ok": True}