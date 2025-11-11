from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator

import json

class Settings(BaseSettings):
    # DB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "contact_share"

    # Auth
    JWT_SECRET: str = "dev-secret"
    JWT_REFRESH_SECRET: str = "dev-refresh-secret"
    MAGIC_TOKEN_SECRET: str = "dev-magic-secret"
    ACCESS_EXPIRES_MIN: int = 30
    REFRESH_EXPIRES_DAYS: int = 14

    # App
    BASE_URL: Optional[AnyHttpUrl] = None

    # CORS
    # Accetta CSV (es. "http://localhost:3000,http://127.0.0.1:3000")
    # o JSON (es. '["http://localhost:3000","http://127.0.0.1:3000"]')
    CORS_ORIGINS: List[str] = []
    CORS_ORIGIN_REGEX: Optional[str] = r"https?://(localhost|127\.0\.0\.1)(:\d+)?$"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None or v == "":
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                # JSON list
                try:
                    data = json.loads(s)
                    if isinstance(data, list):
                        return data
                except Exception:
                    pass
            # CSV fallback
            return [x.strip() for x in s.split(",") if x.strip()]
        return v

    class Config:
        env_file = ".env"

settings = Settings()
