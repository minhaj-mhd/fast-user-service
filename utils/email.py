import smtplib
from email.mime.text import MIMEText
from core.config import settings

def send_verification_email(email_to: str, token: str):
    subject = "Verify Your Email"
    body = f"Click the link to verify: http://localhost:8000/verify/{token}"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = email_to

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")