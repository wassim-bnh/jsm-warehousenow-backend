from fastapi import APIRouter

from warehouse.models import LocationRequest, ResponseModel
from warehouse.warehouse_service import fetch_warehouses_from_airtable, find_nearby_warehouses


warehouse_router = APIRouter()


@warehouse_router.get("/warehouses")
async def warehouses():
    data = await fetch_warehouses_from_airtable()
    return ResponseModel(status="success", data=data)


@warehouse_router.post("/nearby_warehouses")
async def nearby_warehouses(request: LocationRequest):
    nearby_warehouses = await find_nearby_warehouses(request.zip_code, request.radius_miles)
    return ResponseModel(status="success", data=nearby_warehouses)
   