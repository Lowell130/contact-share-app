import asyncio
from app.email import send_email
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    print("📧 Testing Email Sending...")
    print(f"Host: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
    print(f"User: {settings.SMTP_USER}")
    
    try:
        await send_email(
            "pro@example.com", # We can't really check inbox, but we check if SMTP accepts it.
            # Ideally user should check their *real* email, but here we test the connection.
            # Let's try sending to the sender itself for test
            "Test Subject", 
            "<p>This is a test email</p>"
        )
        print("✅ Email sent successfully (according to SMTP server)")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    asyncio.run(main())
