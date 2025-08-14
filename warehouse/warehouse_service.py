import os
import json
import googlemaps
from openai import BaseModel
import redis
import httpx

from geolocation.geolocation_service import get_coordinates, get_driving_distance_mapbox, haversine
from warehouse.models import WarehouseData

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
async def find_nearby_warehouses(origin_zip: str, radius_miles: float):
    origin_coords = get_coordinates(origin_zip)
    if not origin_coords:
        return {"error": "Invalid ZIP code"}
    
    warehouses = await fetch_warehouses_from_airtable()
    nearby = []

    for wh in warehouses:
        wh_zip = wh["fields"].get("Zip")
        if not wh_zip:
            continue

        wh_coords = get_coordinates(wh_zip)
        if not wh_coords:
            continue

        # Use Mapbox driving distance TODO migrate to google maps
        distance = await get_driving_distance_mapbox(origin_coords, wh_coords)
        if distance is None:
            continue

        if distance <= radius_miles:
            wh_copy = wh.copy()
            wh_copy["distance_miles"] = distance
            nearby.append(wh_copy)

    nearby.sort(key=lambda x: x["distance_miles"])
    return {"origin_zip": origin_zip, "warehouses": nearby}
