import re, secrets, string
from datetime import datetime, timezone
from fastapi import UploadFile
import shutil
from pathlib import Path

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

_slug_re = re.compile(r"[^a-z0-9-]+")

def slugify(s: str) -> str:
    s = s.lower().strip().replace(" ", "-")
    s = _slug_re.sub("", s)
    return s or rand_slug()

def rand_slug(n=6):
    chars = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(n))

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
