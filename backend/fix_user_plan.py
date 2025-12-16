"""
Script per verificare e aggiornare manualmente un utente a PRO dopo un pagamento test.
Usa questo script quando il webhook non viene ricevuto in sviluppo locale.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
import asyncio

# Configurazione
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "contact_share"

async def update_user_to_pro(email: str):
    """Aggiorna un utente a PRO manualmente"""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    
    # Trova l'utente
    user = await db.users.find_one({"email": email})
    
    if not user:
        print(f"❌ Utente con email '{email}' non trovato!")
        return
    
    print(f"✅ Utente trovato: {user.get('name')} ({email})")
    print(f"   Piano attuale: {user.get('plan', 'free')}")
    
    # Aggiorna a PRO
    result = await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "plan": "pro",
            "subscription_status": "active",
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.modified_count > 0:
        print(f"✅ Utente aggiornato a PRO!")
        
        # Verifica
        updated_user = await db.users.find_one({"_id": user["_id"]})
        print(f"   Nuovo piano: {updated_user.get('plan')}")
        print(f"   Status: {updated_user.get('subscription_status')}")
    else:
        print(f"⚠️ Nessuna modifica effettuata")
    
    client.close()

async def list_recent_users():
    """Mostra gli ultimi utenti registrati"""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    
    print("\n📋 Ultimi 5 utenti registrati:\n")
    
    cursor = db.users.find().sort("created_at", -1).limit(5)
    users = await cursor.to_list(length=5)
    
    for i, user in enumerate(users, 1):
        print(f"{i}. {user.get('name')} ({user.get('email')})")
        print(f"   Piano: {user.get('plan', 'free')}")
        print(f"   Registrato: {user.get('created_at')}")
        print()
    
    client.close()

if __name__ == "__main__":
    import sys
    
    print("🔧 Script di Aggiornamento Utente a PRO\n")
    
    if len(sys.argv) < 2:
        print("Uso: python fix_user_plan.py <email>")
        print("\nOppure per vedere gli ultimi utenti:")
        print("python fix_user_plan.py --list\n")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        asyncio.run(list_recent_users())
    else:
        email = sys.argv[1]
        asyncio.run(update_user_to_pro(email))
