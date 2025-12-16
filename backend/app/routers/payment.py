from fastapi import APIRouter, Depends, HTTPException, Request, Header
from ..deps import get_current_user
from ..config import settings
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
            success_url=f'{settings.FRONTEND_URL}/payment/success',
            cancel_url=f'{settings.FRONTEND_URL}/payment/cancel',
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
    
    print("🔔 Webhook received!")  # Debug log
    
    if not config:
        print("❌ No config found in database")
        return {} # Silent fail per sicurezza
    
    endpoint_secret = config.get("stripe_webhook_secret")
    if not endpoint_secret:
        print("❌ No webhook secret configured")
        return {}
    
    payload = await request.body()
    print(f"📦 Payload size: {len(payload)} bytes")

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
        print(f"✅ Webhook signature verified")
    except ValueError as e:
        print(f"❌ Invalid payload: {e}")
        raise HTTPException(400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print(f"❌ Invalid signature: {e}")
        raise HTTPException(400, detail="Invalid signature")

    event_type = event['type']
    print(f"📨 Event type: {event_type}")

    # Handle checkout completion
    if event_type == 'checkout.session.completed':
        session = event['data']['object']
        print(f"💳 Checkout session: {session.get('id')}")
        
        # Fulfill the purchase
        user_id = session.get("client_reference_id") or session.get("metadata", {}).get("user_id")
        print(f"👤 User ID from session: {user_id}")
        
        if user_id:
            from bson import ObjectId
            
            # Get customer_id and subscription_id from session
            customer_id = session.get('customer')
            subscription_id = session.get('subscription')
            
            print(f"🆔 Customer ID: {customer_id}")
            print(f"🆔 Subscription ID: {subscription_id}")
            
            result = await db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {
                    "plan": "pro",
                    "stripe_customer_id": customer_id,
                    "stripe_subscription_id": subscription_id,
                    "subscription_status": "active",
                    "updated_at": now_utc()
                }}
            )
            
            print(f"✅ User updated: matched={result.matched_count}, modified={result.modified_count}")
        else:
            print("⚠️ No user_id found in session!")

    # Handle subscription deletion (cancellation)
    elif event_type == 'customer.subscription.deleted':
        subscription = event['data']['object']
        subscription_id = subscription['id']
        
        print(f"🗑️ Subscription deleted: {subscription_id}")
        
        # Find user by subscription_id
        user = await db.users.find_one({"stripe_subscription_id": subscription_id})
        if user:
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "plan": "free",
                    "subscription_status": "canceled",
                    "updated_at": now_utc()
                }}
            )
            print(f"✅ User downgraded to free")
        else:
            print(f"⚠️ No user found with subscription_id: {subscription_id}")

    # Handle subscription updates
    elif event_type == 'customer.subscription.updated':
        subscription = event['data']['object']
        subscription_id = subscription['id']
        status = subscription['status']  # active, canceled, past_due, etc.
        
        print(f"🔄 Subscription updated: {subscription_id}, status: {status}")
        
        user = await db.users.find_one({"stripe_subscription_id": subscription_id})
        if user:
            # If status is "active", user is PRO
            new_plan = "pro" if status == "active" else "free"
            
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "plan": new_plan,
                    "subscription_status": status,
                    "updated_at": now_utc()
                }}
            )
            print(f"✅ User plan updated to: {new_plan}")
        else:
            print(f"⚠️ No user found with subscription_id: {subscription_id}")

    print("✅ Webhook processed successfully")
    return {"status": "success"}


@router.post("/portal")
async def create_portal_session(user=Depends(get_current_user)):
    """Create a Stripe Customer Portal session for subscription management"""
    db = get_db()
    
    # Get Stripe configuration
    config = await get_stripe_config(db)
    stripe.api_key = config["stripe_secret_key"]
    
    # Get user's customer_id
    from bson import ObjectId
    user_doc = await db.users.find_one({"_id": ObjectId(user["id"])})
    
    if not user_doc or not user_doc.get("stripe_customer_id"):
        raise HTTPException(400, detail="No active subscription found")
    
    # Create portal session
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=user_doc["stripe_customer_id"],
            return_url=f'{settings.FRONTEND_URL}/account',
        )
        return {"url": portal_session.url}
    except Exception as e:
        raise HTTPException(400, detail=str(e))

