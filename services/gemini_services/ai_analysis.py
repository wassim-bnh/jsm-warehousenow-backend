import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def analyze_warehouse_with_gemini(warehouses: list[dict]) -> str:
    """
    Generate a holistic AI analysis of the entire warehouse search results.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are analyzing the results of a warehouse search for logistics optimization.  
    The system returned {len(warehouses)} warehouses, ranked based on tier priority
    (Gold > Silver > Bronze) and then by distance/time.

    Here is the ranked warehouse data (in order):
    {[
        {
            "Name": wh["fields"].get("Name"),
            "Tier": wh["fields"].get("Tier"),
            "Distance (miles)": wh.get("distance_miles"),
            "Driving time (minutes)": wh.get("duration_minutes"),
            "Has missing fields": wh.get("has_missed_fields")
        }
        for wh in warehouses
    ]}

    Please provide a short, holistic businesslike summary (3–5 sentences max) explaining:
    1. Why the top warehouses were ranked first.  
    2. How tier vs. distance/time influenced the ranking.  
    3. Any concerns with missing data fields that might affect decision-making.  

    Keep the response clear and factual.
    """

    response = await model.generate_content_async(prompt)
    return response.text.strip()
