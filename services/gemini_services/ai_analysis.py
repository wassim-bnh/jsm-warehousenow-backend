import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


async def analyze_warehouse_with_gemini(warehouse: dict, rank: int, total: int) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are analyzing warehouse ranking for logistics optimization.
    This warehouse has the following details:
    {warehouse['fields']}

    Rank: {rank} out of {total}
    Tier: {warehouse['fields'].get('Tier')}
    Distance: {warehouse.get('distance_miles', 'N/A')} miles
    Driving time: {warehouse.get('duration_minutes', 'N/A')} minutes

    Explain briefly (2–3 sentences max) why this warehouse was ranked #{rank}.
    Highlight tier first (Gold > Silver > Bronze), then distance/time considerations.
    Be factual, concise, and businesslike.
    """
    response = await model.generate_content_async(prompt)
    return response.text.strip()
