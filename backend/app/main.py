from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import ensure_indexes
from .routers import auth, me, cards, public, share, analytics
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .limiter import limiter

app = FastAPI(title="Contact Share API", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Rete di sicurezza per preflight OPTIONS (utile in dev/proxy)
@app.options("/{full_path:path}")
def preflight_handler(full_path: str):
    return Response(status_code=204)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(me.router)
app.include_router(cards.router)    # /cards/{id} (privato)
app.include_router(public.router)   # /public/cards/{slug} (pubblico)
app.include_router(share.router)
app.include_router(analytics.router)

@app.on_event("startup")
async def startup():
    print("CORS allow_origins:", settings.CORS_ORIGINS or ["http://localhost:3000", "http://127.0.0.1:3000"])
    print("CORS allow_origin_regex:", settings.CORS_ORIGIN_REGEX)
    await ensure_indexes()

@app.get("/")
def health():
    return {"ok": True, "name": "contact-share-api"}
