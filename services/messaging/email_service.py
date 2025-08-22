


from warehouse.models import SendEmailData
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
    
    if not email_data.services:
        services_str = "general warehousing services"
    elif len(email_data.services) == 1:
        services_str = email_data.services[0]
    else:
        services_str = ", ".join(email_data.services[:-1]) + f" and {email_data.services[-1]}"

    # Construct subject & body
    subject = f"Request for {services_str} near {email_data.adress}"
    body = f"""Hi, 

We have a request and would like to know if you can help with this.
Please provide the following info below:
Pricing:
Commodity:
Loading method: palletized / slip sheets / floor loaded
Pictures attached below:
Best,
WarehouseNow Team
        """

    # Build message
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email_data.email
    message["Subject"] = subject
    message.set_content(body)

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