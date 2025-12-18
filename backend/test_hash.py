from passlib.context import CryptContext
import sys

print("Testing passlib + bcrypt...")
try:
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    h = pwd_ctx.hash("password")
    print(f"Hash success: {h}")
    v = pwd_ctx.verify("password", h)
    print(f"Verify success: {v}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
