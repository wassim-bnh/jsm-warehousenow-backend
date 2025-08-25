


from warehouse.models import SendBulkEmailData, SendEmailData
import aiosmtplib
from email.message import EmailMessage
from warehouse.models import SendEmailData
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")    
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

async def send_bulk_email(send_bulk_emails: SendBulkEmailData):
    results = []
    for email_data in send_bulk_emails.emails_data:
        subject = send_bulk_emails.email_subject
        body = send_bulk_emails.email_body
        result = await send_email(subject, body, email_data)
        results.append(result)
    return results

async def send_email(email_subject: str, email_body: str, email_data: SendEmailData):
    """
    Send a single email using SMTP
    """
    if not email_data.services:
        services_str = "general warehousing services"
    elif len(email_data.services) == 1:
        services_str = email_data.services[0]
    else:
        services_str = ", ".join(email_data.services[:-1]) + f" and {email_data.services[-1]}"

    # Construct subject
    subject = email_subject or f"Request for {services_str} near {email_data.adress}"

    # Default HTML body
    if not email_body:
        email_body = """\
        <html>
          <body>
            <p>Hi,</p>

            <p>We have a request and would like to know if you can help with this.</p>

            <p>Please provide pricing based on the following info below:</p>

            <p>
              <b>Commodity:</b><br>
              <b>Loading method:</b> palletized / slip sheets / floor loaded
            </p>

            <p>Pictures attached below:</p>

            <p>Best,<br>
            WarehouseNow Team</p>
          </body>
        </html>
        """

    # Build message
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email_data.email
    message["Subject"] = subject

    # Add plain-text fallback + HTML version
    message.set_content("Please view this email in HTML mode.")
    message.add_alternative(email_body, subtype="html")

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