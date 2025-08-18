import os
from fastapi import APIRouter
from pydantic import BaseModel

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
CACHE_KEY_WAREHOUSES = "warehouses_cache"
CACHE_TTL = 600  # seconds

geolocation_router = APIRouter()


