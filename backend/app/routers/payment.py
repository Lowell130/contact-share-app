from fastapi import APIRouter, Depends, HTTPException, Request, Header
from ..deps import get_current_user
from ..db import get_db
from ..utils import now_utc
import stripe
import json

router = APIRouter(prefix="/payment", tags=["payment"])

async def get_stripe_config(db):
    settings = await db.settings.find_one({"_id": "config"})
    if not settings or not settings.get("stripe_secret_key"):
        raise HTTPException(500, detail="Stripe not configured")
    return settings

@router.post("/checkout")
async def create_checkout_session(user=Depends(get_current_user)):
    db = get_db()
    
    # 1. Get Config
    config = await get_stripe_config(db)
    stripe.api_key = config["stripe_secret_key"]
    price_id = config.get("stripe_price_id")
    
    if not price_id:
        raise HTTPException(500, detail="Price ID not configured")

    # 2. Create Session
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='http://localhost:3000/payment/success', # TODO: Env var for base URL
            cancel_url='http://localhost:3000/payment/cancel',
            client_reference_id=str(user["id"]),
            customer_email=user["email"],
            metadata={
                 "user_id": str(user["id"])
            }
        )
    except Exception as e:
         raise HTTPException(400, detail=str(e))

    return {"url": checkout_session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    db = get_db()
    config = await db.settings.find_one({"_id": "config"})
    
    if not config:
        return {} # Silent fail per sicurezza
        
    endpoint_secret = config.get("stripe_webhook_secret")
    payload = await request.body()

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
    except ValueError as e:
        raise HTTPException(400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(400, detail="Invalid signature")

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Fulfill the purchase
        user_id = session.get("client_reference_id") or session.get("metadata", {}).get("user_id")
        if user_id:
             from bson import ObjectId
             await db.users.update_one(
                 {"_id": ObjectId(user_id)},
                 {"$set": {"plan": "pro", "updated_at": now_utc()}}
             )

    return {"status": "success"}
