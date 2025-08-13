import os
import httpx
import asyncio


import os
import base64
import httpx
import asyncio

ATLASSIAN_EMAIL = os.getenv("ATLASSIAN_EMAIL") 
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN") 
WORKSPACE_ID = os.getenv("ATLASSIAN_WORKSPACE_ID") 
SCHEMA_KEY = "WHDB"

async def fetch_schema_list():
    # Prepare Basic Auth header
    auth_str = f"{ATLASSIAN_EMAIL}:{ATLASSIAN_API_TOKEN}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Accept": "application/json"
    }

    url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/v1/objectschema/list"


    headers = {
    "Accept": "application/json"
    }
        
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(resp.status_code, resp.text)
        resp.raise_for_status()
        return resp.json()

async def fetch_all_objects():
    auth_str = f"{ATLASSIAN_EMAIL}:{ATLASSIAN_API_TOKEN}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Accept": "application/json"
    }

    base_url = f"https://api.atlassian.com/jsm/assets/workspace/{WORKSPACE_ID}/object"
    params = {
        "objectSchemaKey": SCHEMA_KEY,
        "limit": 100,
        "startAt": 0
    }

    all_objects = []

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            values = data.get("values", [])
            all_objects.extend(values)

            if data.get("isLast", True):
                break

            params["startAt"] += params["limit"]

    return all_objects

if __name__ == "__main__":
     warehouses = asyncio.run(fetch_all_objects())
     print(warehouses)
