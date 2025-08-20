from fastapi import APIRouter

from services.messaging.email_service import send_bulk_email
from warehouse.models import LocationRequest, ResponseModel, SendEmailData
from warehouse.warehouse_service import fetch_warehouses_from_airtable, find_nearby_warehouses


warehouse_router = APIRouter()


@warehouse_router.get("/warehouses")
async def warehouses():
    data = await fetch_warehouses_from_airtable()
    return ResponseModel(status="success", data=data)


@warehouse_router.post("/nearby_warehouses")
async def find_nearby_warehouses_endpoint(request: LocationRequest):
    nearby_warehouses = await find_nearby_warehouses(request.zip_code, request.radius_miles)
    return ResponseModel(status="success", data=nearby_warehouses)
   
@warehouse_router.post("/send_email")
async def send_bulk_email_endpoint(emails_data: list[SendEmailData]):
    response = await send_bulk_email(emails_data)
    return ResponseModel(status="success", data=response)