import os
from typing import List

from pydantic import BaseModel
import httpx

from services.geolocation.geolocation_service import get_coordinates, get_driving_distance_and_time_mapbox
from warehouse.models import WarehouseData
from services.gemini_services.ai_analysis import analyze_warehouse_with_gemini

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
    """Return a list of field names that are empty or missing."""
    missing = []
    for key, value in fields.items():
        if value in (None, "", [], {}):
            missing.append(key)
    return missing


async def find_nearby_warehouses(origin_zip: str, radius_miles: float):
    origin_coords = get_coordinates(origin_zip)
    if not origin_coords:
        return {"error": "Invalid ZIP code"}

    warehouses: List[WarehouseData] = await fetch_warehouses_from_airtable()
    nearby = []

    for wh in warehouses:
        wh_zip = wh["fields"].get("Zip")
        if not wh_zip:
            continue

        wh_coords = get_coordinates(wh_zip)
        if not wh_coords:
            continue

        result = await get_driving_distance_and_time_mapbox(origin_coords, wh_coords)
        if not result:
            continue

        distance_miles = result["distance_miles"]
        duration_minutes = result["duration_minutes"]

        if distance_miles <= radius_miles:
            wh_copy = wh.copy()
            wh_copy["distance_miles"] = distance_miles
            wh_copy["duration_minutes"] = duration_minutes
            wh_copy["tier_rank"] = _tier_rank(wh["fields"].get("Tier"))

            wh_copy["tags"] = find_missing_fields(wh["fields"])
            if wh_copy["tags"]:
                wh_copy["has_missed_fields"] = True
            else: 
                wh_copy["has_missed_fields"] = False
            nearby.append(wh_copy)

    nearby.sort(key=lambda x: (x["tier_rank"], x["distance_miles"]))

    for idx, wh in enumerate(nearby, start=1):
        wh["ai_analysis"] = await analyze_warehouse_with_gemini(wh, idx, len(nearby))

    return {"origin_zip": origin_zip, "warehouses": nearby}


