from fastapi import APIRouter, HTTPException, Request
from ..db import get_db
from ..utils import now_utc
from ..services.vcard import to_vcard
from fastapi.responses import Response

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
        "notes": c.get("notes", ""),              # <-- AGGIUNTO
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
        "card_id": str(c["_id"]), "type": "vcard_download",
        "ua": request.headers.get("user-agent"),
        "ref": request.headers.get("referer"),
        "ts": now_utc()
    })
    vcf = to_vcard(c.get("title") or "Contact", c.get("fields", []))
    headers = {"Content-Disposition": f'attachment; filename="{c["slug"]}.vcf"'}
    return Response(content=vcf, media_type="text/vcard", headers=headers)
