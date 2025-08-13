
import os
from typing import List


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

from fastapi import HTTPException
import httpx


async def get_distances(origins: str, destinations: List[str]) -> List[float]:
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origins,
        "destinations": "|".join(destinations),
        "key": GOOGLE_MAPS_API_KEY,
        "units": "metric",
        "mode": "driving"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Google Maps Distance Matrix API error")

    data = response.json()
    if data.get("status") != "OK":
        raise HTTPException(status_code=400, detail="Invalid response from Google Maps API")

    distances = []
    rows = data.get("rows", [])
    if not rows or not rows[0].get("elements"):
        raise HTTPException(status_code=400, detail="No distance data available")

    elements = rows[0]["elements"]
    for el in elements:
        if el.get("status") == "OK":
            distances.append(el["distance"]["value"])
        else:
            distances.append(float('inf'))
    return distances