# helpers/email_ai.py
from typing import Dict
import google.generativeai as genai
import os

# Load your Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

async def generate_email_prompt(warehouse: Dict) -> Dict[str, str]:
    """
    Generate a subject and body for contacting a warehouse about availability.
    warehouse: a dict containing warehouse data from Airtable
    Returns: dict with { "subject": str, "body": str }
    """
    name = warehouse["fields"].get("Name", "the warehouse")
    city = warehouse["fields"].get("City", "")
    state = warehouse["fields"].get("State", "")
    services = warehouse["fields"].get("Services", [])
    tier = warehouse["fields"].get("Tier", "N/A")

    services_str = ", ".join(services) if services else "general warehousing services"

    # ✅ Prompt crafted for Gemini
    prompt = f"""
    You are helping me write a professional outreach email to a warehouse.

    Context:
    - Warehouse Name: {name}
    - Location: {city}, {state}
    - Tier: {tier}
    - Services: {services_str}

    Task:
    1. Generate a **short subject line** (under 8 words) that is polite and professional, asking about availability.
    2. Generate a **short email body** (100-150 words) that:
        - Introduces my company as seeking storage/warehouse services.
        - Politely asks if this warehouse is available for new clients.
        - References the warehouse name and city to make it personalized.
        - Requests further details on capacity, pricing, and services if available.
        - Ends with a polite thank you and a request to reply.

    Return the result in strict JSON format:
    {{
      "subject": "...",
      "body": "..."
    }}
    """

    # Call Gemini model
    model = genai.GenerativeModel("gemini-pro")
    response = await model.generate_content_async(prompt)

    try:
        # Parse JSON safely
        text = response.text.strip()
        result = eval(text) if text.startswith("{") else {"subject": "Warehouse Availability", "body": text}
        return result
    except Exception:
        return {
            "subject": f"Availability inquiry - {name}",
            "body": f"Hello,\n\nI would like to inquire if {name} located in {city}, {state} is currently available for new clients. Please share details on capacity, pricing, and services.\n\nThank you!"
        }
