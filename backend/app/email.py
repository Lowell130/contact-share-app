import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from fastapi.concurrency import run_in_threadpool

def _send_sync(to_email: str, subject: str, html_content: str):
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAILS_FROM, to_email, msg.as_string())
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        raise e

async def send_email(to_email: str, subject: str, html_content: str):
    await run_in_threadpool(_send_sync, to_email, subject, html_content)
