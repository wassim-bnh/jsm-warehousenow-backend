import os
from typing import List

from pydantic import BaseModel
import httpx
import copy

from services.geolocation.geolocation_service import get_coordinates_mapbox, get_driving_distance_and_time_mapbox, get_coordinates_google, get_driving_distance_and_time_google
from warehouse.models import FilterWarehouseData, WarehouseData
from services.gemini_services.ai_analysis import GENERAL_AI_ANALYSIS, analyze_warehouse_with_gemini
from dotenv import load_dotenv

load_dotenv()
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = "Imported table" 
VIEW_NAME = "warehouse"        


#GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
#gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

class LocationRequest(BaseModel):
    zip_code: str
    radius_miles: float = 50  # default to 50 miles
    
async def fetch_warehouses_from_airtable() -> list[WarehouseData]:
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}"
    }
    params = {
        "view": VIEW_NAME  # optional
    }

    records = []
    async with httpx.AsyncClient() as client:
        offset = None
        while True:
            if offset:
                params["offset"] = offset
            resp = await client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            records.extend(data.get("records", []))
            offset = data.get("offset")
            if not offset:
                break

    return records

# Find nearby warehouses (openStreetMap)
def _tier_rank(tier: str) -> int:
    """Lower number = higher priority."""
    if not tier:
        return 99
    t = str(tier).strip().lower()
    order = {"gold": 0, "silver": 1, "bronze": 2}
    return order.get(t, 99)

def find_missing_fields(fields: dict) -> List[str]:
    """Return a list of field names that are empty or missing compared to FilterWarehouseData"""
    missing = []
    for field_name in FilterWarehouseData.model_fields.keys():
        value = fields.get(field_name)
        if value in (None, "", [], {}):
            missing.append(field_name)
    return missing

from services.geolocation.geolocation_service import (
    get_coordinates_mapbox,
    get_coordinates_google,
    get_driving_distance_and_time_google,
    haversine,
)

async def find_nearby_warehouses(origin_zip: str, radius_miles: float):
    origin_coords = get_coordinates_mapbox(origin_zip)
    if not origin_coords:
        return {"error": "Invalid ZIP code"}

    warehouses: List[WarehouseData] = await fetch_warehouses_from_airtable()
    nearby: List[WarehouseData] = []

    for wh in warehouses:
        wh_zip = wh["fields"].get("Zip")
        if not wh_zip:
            continue

        wh_coords = get_coordinates_google(wh_zip)
        if not wh_coords:
            continue

        # --- Step 1: Fast prefilter with Haversine ---
        straight_line_miles = haversine(
            origin_coords[0], origin_coords[1],
            wh_coords[0], wh_coords[1]
        )

        if straight_line_miles > radius_miles * 2:
            continue  # Skip if too far, no Google API call

        # --- Step 2: Accurate check with Google API ---
        result = await get_driving_distance_and_time_google(origin_coords, wh_coords)
        if not result:
            continue

        distance_miles = result["distance_miles"]
        duration_minutes = result["duration_minutes"]

        if distance_miles <= radius_miles:
            wh_copy = copy.copy(wh)
            wh_copy["distance_miles"] = distance_miles
            wh_copy["duration_minutes"] = duration_minutes
            wh_copy["tier_rank"] = _tier_rank(wh["fields"].get("Tier"))

            wh_copy["tags"] = find_missing_fields(wh["fields"])
            wh_copy["has_missed_fields"] = bool(wh_copy["tags"])

            nearby.append(wh_copy)

    # --- Sort final list ---
    nearby.sort(key=lambda x: (x["tier_rank"], x["duration_minutes"], x["distance_miles"]))

    # --- AI analysis with fallback ---
    try:
        ai_analysis = await analyze_warehouse_with_gemini(nearby)
    except Exception:
        ai_analysis = GENERAL_AI_ANALYSIS

    return {"origin_zip": origin_zip, "warehouses": nearby, "ai_analysis": ai_analysis}



