import json
from fastapi import APIRouter, HTTPException
from openai import BaseModel
import redis

from geolocation.geolocation_service import get_distances
from jsm_warehouse.jsm_warehouse_service import get_assets_data


warehouse_router = APIRouter()

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

CACHE_KEY = "warehouses_cache"
CACHE_TTL = 600 

class LocationRequest(BaseModel):
    postcode: str

@warehouse_router.get("/warehouses")
async def warehouses():
    cached = await redis_client.get(CACHE_KEY)
    if cached:
        return json.loads(cached)
    
    data = await get_assets_data()
    return data


@warehouse_router.post("/nearby_warehouses")
async def nearby_warehouses(request: LocationRequest):

    warehouses = await get_assets_data()
    if not warehouses:
        raise HTTPException(status_code=404, detail="No warehouses found")

    destinations = []
    for wh in warehouses:
        props = wh.get("properties", {})
        lat = props.get("latitude")
        lng = props.get("longitude")
        if lat is None or lng is None:
            continue
        destinations.append(f"{lat},{lng}")

    distances = await get_distances(request.postcode, destinations)
    warehouses_with_coords = [wh for wh in warehouses if wh.get("properties", {}).get("latitude") and wh.get("properties", {}).get("longitude")]

    warehouse_distances = list(zip(warehouses_with_coords, distances))

    # Sort by distance ascending and pick top 5
    nearest = sorted(warehouse_distances, key=lambda x: x[1])[:5]

    # Add distance to each warehouse dict
    result = []
    for wh, dist in nearest:
        wh_copy = wh.copy()
        wh_copy["distance_meters"] = dist
        result.append(wh_copy)

    return {"nearest_warehouses": result}