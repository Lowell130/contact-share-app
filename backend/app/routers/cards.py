from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File
from pathlib import Path
from bson import ObjectId, errors as bson_errors
from ..deps import get_current_user
from ..db import get_db
from ..models import CardIn, CardOut
from ..utils import now_utc, slugify, rand_slug, save_upload_file
from ..services.vcard import to_vcard
from ..services.qrcode_gen import qrcode_png

router = APIRouter(prefix="/cards", tags=["cards"])

PREMIUM_THEMES = {
    "modern_emerald", "modern_blue", "modern_indigo", "modern_rose", "modern_orange"
}

def card_projection():
    return {
        "_id": 1, "user_id": 1, "title": 1, "slug": 1, "fields": 1, "theme": 1,
        "avatar_url": 1, "is_public": 1, "is_indexed": 1, "allow_vcard": 1, "notes": 1,
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
    if data.theme in PREMIUM_THEMES and user.get("plan") != "pro":
        raise HTTPException(status_code=403, detail="This theme is reserved for Pro plan users.")
    
    # Check Limit
    if user.get("plan") == "free":
        count = await db.cards.count_documents({"user_id": user["id"]})
        if count >= 1:
            raise HTTPException(status_code=403, detail="Free plan limit reached (1 card). Upgrade to Pro.")

    doc = data.model_dump()
    doc.update({
        "user_id": user["id"],
        "slug": slug,
        "created_at": now_utc(),
        "updated_at": now_utc(),
    })
    
    # Fallback avatar se non fornito
    if not doc.get("avatar_url"):
        # Usa DiceBear con lo slug come seed
        doc["avatar_url"] = f"https://api.dicebear.com/7.x/avataaars/svg?seed={slug}"

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
    
    # Check Premium Theme
    if updates.get("theme") and updates["theme"] in PREMIUM_THEMES and user.get("plan") != "pro":
        raise HTTPException(status_code=403, detail="This theme is reserved for Pro plan users.")

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

@router.post("/{id}/avatar", response_model=CardOut)
async def upload_avatar(id: str, file: UploadFile = File(...), user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    c = await db.cards.find_one({"_id": oid, "user_id": user["id"]})
    if not c: raise HTTPException(404, detail="Card not found")

    # Validazione estensione
    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(400, detail="Invalid image format")

    # Salva file
    filename = f"{oid}{ext}"
    upload_dir = Path("static/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / filename
    
    save_upload_file(file, dest)

    # Aggiorna URL (assumiamo che il backend sia servito su / o che static sia accessibile)
    # TODO: In prod meglio usare URL assoluto da env var
    avatar_url = f"/static/uploads/{filename}"
    
    await db.cards.update_one(
        {"_id": oid},
        {"$set": {"avatar_url": avatar_url, "updated_at": now_utc()}}
    )
    
    c = await db.cards.find_one({"_id": oid}, card_projection())
    c["id"] = str(c["_id"]); c["user_id"] = str(c["user_id"])
    return c

@router.delete("/{id}/avatar", response_model=CardOut)
async def delete_avatar(id: str, user=Depends(get_current_user)):
    db = get_db()
    oid = to_object_id_or_404(id)
    c = await db.cards.find_one({"_id": oid, "user_id": user["id"]})
    if not c: raise HTTPException(404, detail="Card not found")

    # Se c'è un avatar custom (locale), potremmo cancellare il file
    # Ma per ora basta resettare l'URL
    # Se l'URL inizia con /static/uploads/, potremmo cancellarlo dal disco
    old_url = c.get("avatar_url", "")
    if old_url and old_url.startswith("/static/uploads/"):
        try:
            # Rimuovi file fisico
            filename = old_url.split("/")[-1]
            path = Path("static/uploads") / filename
            if path.exists():
                path.unlink()
        except Exception:
            pass # Ignora errori di cancellazione file

    # Reset a DiceBear
    slug = c.get("slug") or rand_slug()
    new_avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={slug}"
    
    await db.cards.update_one(
        {"_id": oid},
        {"$set": {"avatar_url": new_avatar, "updated_at": now_utc()}}
    )
    
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
