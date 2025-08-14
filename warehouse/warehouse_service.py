import os
import json
import googlemaps
from openai import BaseModel
import redis
import httpx

from geolocation.geolocation_service import get_coordinates, haversine

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = "Imported table" 
VIEW_NAME = "warehouse"        


#GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
#gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

class LocationRequest(BaseModel):
    zip_code: str
    radius_miles: float = 50  # default to 50 miles
    
async def fetch_warehouses_from_airtable() -> list:
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
    
    origin_lat, origin_lon = origin_coords
    warehouses = await fetch_warehouses_from_airtable()
    
    nearby = []
    for wh in warehouses:
        wh_zip = wh["fields"].get("Zip")  
        if not wh_zip:
            continue
        wh_coords = get_coordinates(wh_zip)
        if not wh_coords:
            continue
        wh_lat, wh_lon = wh_coords
        distance = haversine(origin_lat, origin_lon, wh_lat, wh_lon)
        if distance <= radius_miles:
            wh_copy = wh.copy()
            wh_copy["distance_miles"] = distance
            nearby.append(wh_copy)
    
    nearby.sort(key=lambda x: x["distance_miles"])
    return {"origin_zip": origin_zip, "warehouses": nearby}

'''
# Find nearby warehouses(google maps)
async def find_nearby_warehouses_google(origin_zip: str, radius_miles: float):
    warehouses = await fetch_warehouses_from_airtable()
     # Geocode the input zip code
    geocode_result = gmaps.geocode(httpx.request.zip_code)
    if not geocode_result:
        return {"error": "Invalid zip code"}
    user_location = geocode_result[0]["geometry"]["location"]
    user_lat, user_lng = user_location["lat"], user_location["lng"]

    nearby = []

    for wh in warehouses:
        wh_zip = wh["fields"].get("Zip")
        if not wh_zip:
            continue
        
        # Geocode warehouse zip
        wh_geocode = gmaps.geocode(str(wh_zip))
        if not wh_geocode:
            continue
        wh_location = wh_geocode[0]["geometry"]["location"]
        wh_lat, wh_lng = wh_location["lat"], wh_location["lng"]

        distance = haversine(user_lat, user_lng, wh_lat, wh_lng)
        if distance <= httpx.request.radius_miles:
            wh_copy = wh.copy()
            wh_copy["distance_miles"] = round(distance, 2)
            nearby.append(wh_copy)

    return {"count": len(nearby), "warehouses": nearby} 
'''