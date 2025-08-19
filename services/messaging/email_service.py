


from warehouse.models import SendEmailData
import aiosmtplib
from email.message import EmailMessage
from warehouse.models import SendEmailData
from services.gemini_services.generate_email import generate_email_prompt
import os


SMTP_HOST = os.getenv("SMTP_HOST")    
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

async def send_bulk_email(emails_data: list[SendEmailData]):
    results = []
    for email_data in emails_data:
        result = await send_email(email_data)
        results.append(result)
    return results

async def send_email(email_data: SendEmailData):
    """
    Send a single email using SMTP
    """
    ai_email = await generate_email_prompt(
            warehouse_name=email_data.warehouse_name,
            contact_name=email_data.contact_name
        )
    email_data.subject = email_data.subject or ai_email["subject"]
    email_data.body = email_data.body or ai_email["body"]
    
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email_data.email
    message["Subject"] = email_data.subject
    
    if email_data.cc:
        message["Cc"] = ", ".join(email_data.cc)
    if email_data.bcc:
        message["Bcc"] = ", ".join(email_data.bcc)

    message.set_content(email_data.body)

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASS,
        )
        return {"status": "success", "to": email_data.email}
    except Exception as e:
        return {"status": "error", "to": email_data.email, "error": str(e)}