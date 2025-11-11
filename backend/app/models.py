from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal, Any
from datetime import datetime

class UserIn(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    name: Optional[str] = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
    plan: Optional[str] = "free"
    created_at: datetime

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"

class CardField(BaseModel):
    type: str
    label: str
    value: str
    visible: bool = True

class CardIn(BaseModel):
    title: str
    slug: Optional[str] = None
    fields: List[CardField] = []
    theme: Optional[dict] = None
    avatar_url: Optional[str] = None
    is_public: bool = True
    allow_vcard: bool = True
    notes: Optional[str] = None

class CardOut(CardIn):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class ShareIn(BaseModel):
    card_id: str
    expires_minutes: int = 60
    password: Optional[str] = None

class ShareOut(BaseModel):
    id: str
    slug: str
    url: str
    expires_at: datetime

class MagicRequestIn(BaseModel):
    email: EmailStr

class MagicConfirmIn(BaseModel):
    token: str

class AnalyticsSummary(BaseModel):
    total_views: int
    total_vcard: int
    last30d: List[dict]
