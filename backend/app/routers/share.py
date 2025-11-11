from fastapi import APIRouter, HTTPException, Depends, Request
from bson import ObjectId
from datetime import timedelta
from ..deps import get_current_user
from ..db import get_db
from ..models import ShareIn, ShareOut
from ..utils import now_utc, rand_slug
from ..security import hash_password, verify_password

router = APIRouter(prefix="/share", tags=["share"])

@router.post("", response_model=ShareOut)
async def create_share(data: ShareIn, user=Depends(get_current_user)):
    db = get_db()
    card = await db.cards.find_one({"_id": ObjectId(data.card_id), "user_id": user["id"]})
    if not card: raise HTTPException(404, detail="Card not found")
    slug = rand_slug(8)
    expires_at = now_utc() + timedelta(minutes=max(1, data.expires_minutes))
    doc = {
        "card_id": str(card["_id"]),
        "slug": slug,
        "expires_at": expires_at,
        "password_hash": hash_password(data.password) if data.password else None,
        "created_at": now_utc()
    }
    r = await db.share_links.insert_one(doc)
    url = f"/s/{slug}"
    return ShareOut(id=str(r.inserted_id), slug=slug, url=url, expires_at=expires_at)

@router.get("/s/{slug}")
async def resolve_share(slug: str, request: Request, password: str | None = None):
    db = get_db()
    link = await db.share_links.find_one({"slug": slug})
    if not link: raise HTTPException(404)
    if link.get("password_hash") and not password:
        raise HTTPException(status_code=401, detail="Password required")
    if link.get("password_hash") and password and not verify_password(password, link["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")
    card = await db.cards.find_one({"_id": ObjectId(link["card_id"])})
    if not card: raise HTTPException(404)
    # non cambia lo stato di pubblica/privata: è “pass-through” temporaneo
    return {"slug": card["slug"]}
