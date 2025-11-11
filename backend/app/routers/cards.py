from fastapi import APIRouter, Depends, HTTPException, Response
from bson import ObjectId, errors as bson_errors
from ..deps import get_current_user
from ..db import get_db
from ..models import CardIn, CardOut
from ..utils import now_utc, slugify, rand_slug
from ..services.vcard import to_vcard
from ..services.qrcode_gen import qrcode_png

router = APIRouter(prefix="/cards", tags=["cards"])

def card_projection():
    return {
        "_id": 1, "user_id": 1, "title": 1, "slug": 1, "fields": 1, "theme": 1,
        "avatar_url": 1, "is_public": 1, "allow_vcard": 1, "notes": 1,
        "created_at": 1, "updated_at": 1
    }

def to_object_id_or_404(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except bson_errors.InvalidId:
        # Se qualcuno chiama /cards/<slug>, evitiamo 500 e rispondiamo 404
        raise HTTPException(status_code=404, detail="Card not found")

@router.get("", response_model=list[CardOut])
async def list_cards(user=Depends(get_current_user)):
    db = get_db()
    cur = db.cards.find({"user_id": user["id"]}, card_projection()).sort("created_at", -1)
    out = []
    async for c in cur:
        c["id"] = str(c["_id"]); c["user_id"] = str(c["user_id"])
        out.append(c)
    return out

@router.post("", response_model=CardOut)
async def create_card(data: CardIn, user=Depends(get_current_user)):
    db = get_db()
    slug = slugify(data.slug or data.title) or rand_slug()
    if await db.cards.find_one({"slug": slug}):
        slug = f"{slug}-{rand_slug(3)}"
    doc = data.model_dump()
    doc.update({
        "user_id": user["id"],
        "slug": slug,
        "created_at": now_utc(),
        "updated_at": now_utc(),
    })
    res = await db.cards.insert_one(doc)
    doc["id"] = str(res.inserted_id)
    return CardOut(**doc)

@router.get("/{id}", response_model=CardOut)
async def get_card(id: str, user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    c = await db.cards.find_one({"_id": oid, "user_id": user["id"]}, card_projection())
    if not c: raise HTTPException(404, detail="Card not found")
    c["id"] = str(c["_id"]); c["user_id"] = str(c["user_id"])
    return c

@router.put("/{id}", response_model=CardOut)
async def update_card(id: str, data: CardIn, user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    c = await db.cards.find_one({"_id": oid, "user_id": user["id"]})
    if not c: raise HTTPException(404, detail="Card not found")
    updates = data.model_dump()
    # gestione slug se passato
    if updates.get("slug"):
        new_slug = slugify(updates["slug"])
        exist = await db.cards.find_one({"slug": new_slug, "_id": {"$ne": oid}})
        if exist: raise HTTPException(409, detail="Slug already in use")
        updates["slug"] = new_slug
    updates["updated_at"] = now_utc()
    await db.cards.update_one({"_id": oid}, {"$set": updates})
    c = await db.cards.find_one({"_id": oid}, card_projection())
    c["id"] = str(c["_id"]); c["user_id"] = str(c["user_id"])
    return c

@router.delete("/{id}")
async def delete_card(id: str, user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    await db.cards.delete_one({"_id": oid, "user_id": user["id"]})
    return {"ok": True}

@router.get("/{id}/vcard")
async def download_vcard(id: str, user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    c = await db.cards.find_one({"_id": oid, "user_id": user["id"]})
    if not c or not c.get("allow_vcard", True): raise HTTPException(404, detail="Card not found")
    fullname = c.get("title") or "Contact"
    vcf = to_vcard(fullname, [*map(lambda d: d, c.get("fields", []))])
    headers = {"Content-Disposition": f'attachment; filename="{c["slug"]}.vcf"'}
    return Response(content=vcf, media_type="text/vcard", headers=headers)

@router.get("/{id}/qrcode")
async def get_qrcode(id: str, user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    c = await db.cards.find_one({"_id": oid, "user_id": user["id"]})
    if not c: raise HTTPException(404, detail="Card not found")
    # link pubblico
    public_url = f"/c/{c['slug']}"
    png = qrcode_png(public_url)
    headers = {"Content-Disposition": f'inline; filename="{c["slug"]}.png"'}
    return Response(content=png, media_type="image/png", headers=headers)
