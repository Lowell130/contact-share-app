from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client: AsyncIOMotorClient | None = None

def get_db():
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGO_URI)
    return client[settings.MONGO_DB]

async def ensure_indexes():
    db = get_db()
    await db.users.create_index("email", unique=True)
    await db.cards.create_index("slug", unique=True)
    await db.cards.create_index("user_id")
    await db.share_links.create_index("slug", unique=True)
    await db.share_links.create_index("expires_at", expireAfterSeconds=0)
    await db.events.create_index("card_id")
    await db.events.create_index("ts")
    await db.magic_tokens.create_index("token", unique=True)
    await db.magic_tokens.create_index("expires_at", expireAfterSeconds=0)
