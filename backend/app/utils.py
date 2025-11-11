import re, secrets, string
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

_slug_re = re.compile(r"[^a-z0-9-]+")

def slugify(s: str) -> str:
    s = s.lower().strip().replace(" ", "-")
    s = _slug_re.sub("", s)
    return s or rand_slug()

def rand_slug(n: int = 6) -> str:
    alpha = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alpha) for _ in range(n))
