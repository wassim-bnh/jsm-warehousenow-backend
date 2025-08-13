

from base64 import b64encode
import base64
import json
import os

from fastapi import HTTPException
import httpx
import redis


ATLASSIAN_EMAIL = os.getenv("ATLASSIAN_EMAIL")
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN") 
WORKSPACE_ID = os.getenv("ATLASSIAN_WORKSPACE_ID") 

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

CACHE_KEY_WAREHOUSES = "warehouses_cache"
CACHE_TTL = 3600  # 1 hour cache expiration

async def fetch_warehouses_from_assets() -> list:
    # Correct JSM Assets API endpoint for listing objects
    url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/object"

    # Prepare Basic Auth
    auth_str = f"{ATLASSIAN_EMAIL}:{ATLASSIAN_API_TOKEN}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(response.status_code, response.text)  # Debug
        response.raise_for_status()
        data = response.json()
        print(data)

    return data.get("values", [])


async def cache_warehouses():
    warehouses = await fetch_warehouses_from_assets()
    # Store as JSON string in Redis
    print(warehouses)
    await redis_client.set(CACHE_KEY_WAREHOUSES, json.dumps(warehouses), ex=CACHE_TTL)


async def get_assets_data():
    warehouses = await fetch_warehouses_from_assets()
    return warehouses