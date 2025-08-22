import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GENERAL_AI_ANALYSIS = """
The warehouse search results show multiple options ranked primarily by tier (Gold > Silver > Bronze) 
and secondarily by driving distance and time. Top-ranked warehouses balance high tier status 
with proximity to the origin zip code. Attention should be paid to any missing data fields, 
as incomplete information may impact decision-making for logistics planning.
"""

async def analyze_warehouse_with_gemini(warehouses: list[dict]) -> str:
    """
    Generate a holistic AI analysis of the entire warehouse search results,
    with explicit justification for the top three warehouses by name.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Build summary data
    warehouse_data = [
        {
            "Name": wh["fields"].get("Name"),
            "Tier": wh["fields"].get("Tier"),
            "Distance (miles)": round(wh.get("distance_miles", 0), 2),
            "Driving time (minutes)": round(wh.get("duration_minutes", 0), 1),
            "Has missing fields": wh.get("has_missed_fields")
        }
        for wh in warehouses
    ]

    # Extract the top 3 for explicit reasoning
    top_three = warehouse_data[:3]

    prompt = f"""
    You are analyzing the results of a warehouse search for logistics optimization.  
    The system returned {len(warehouses)} warehouses, ranked by tier priority
    (Gold > Silver > Bronze) and then by driving time/distance.

    Ranked warehouse data:
    {warehouse_data}

    Focus on the top three warehouses:
    {top_three}

    Please provide a concise businesslike analysis (2-3 sentences) that includes:
    1. Specific justification for why {top_three[0]["Name"]}, {top_three[1]["Name"]}, 
       and {top_three[2]["Name"]} were ranked as the top three.  
    2. How tier vs. distance/time influenced the overall order.  
    3. Any concerns with missing data fields that could affect decision-making.  

    Keep the response factual and clear.
    """

    response = await model.generate_content_async(prompt)
    return response.text.strip()
