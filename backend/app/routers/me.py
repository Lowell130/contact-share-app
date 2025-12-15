from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..models import UserOut
from ..db import get_db

router = APIRouter(tags=["me"])

@router.get("/me", response_model=UserOut)
async def me(user = Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user.get("name"),
        "plan": user.get("plan","free"),
        "created_at": user["created_at"],
    }

@router.put("/me", response_model=UserOut)
async def update_me(payload: dict, user=Depends(get_current_user)):
    db = get_db()
    # "plan" rimosso da qui per sicurezza. Usa l'endpoint di pagamento (o test) per cambiare piano.
    allowed = {k: v for k, v in payload.items() if k in ["name"]}
    await db.users.update_one({"_id": user["_id"]}, {"$set": allowed})
    fresh = await db.users.find_one({"_id": user["_id"]})
    return {
        "id": str(fresh["_id"]),
        "email": fresh["email"],
        "name": fresh.get("name"),
        "plan": fresh.get("plan","free"),
        "created_at": fresh["created_at"],
    }

@router.post("/me/upgrade-test", response_model=UserOut)
async def upgrade_me_test(plan: str = "pro", user=Depends(get_current_user)):
    """
    ENDPOINT DI TEST: Da rimuovere in produzione o proteggere con admin key.
    Permette di cambiare il piano al volo.
    """
    db = get_db()
    await db.users.update_one({"_id": user["_id"]}, {"$set": {"plan": plan}})
    fresh = await db.users.find_one({"_id": user["_id"]})
    return {
        "id": str(fresh["_id"]),
        "email": fresh["email"],
        "name": fresh.get("name"),
        "plan": fresh.get("plan","free"),
        "created_at": fresh["created_at"],
    }
