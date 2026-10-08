from email.message import EmailMessage
import smtplib
from .config import settings

def send_resource_email(recipient: str, subject: str, body: str, attachment_path: str | None = None):
    if not settings.smtp_host or not settings.email_from:
        raise RuntimeError("Email is not configured yet.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = recipient
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf",
                               filename=attachment_path.split("/")[-1])

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.starttls()
        if settings.smtp_username:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(msg)
