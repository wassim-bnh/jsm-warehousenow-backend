from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
import httpx
import requests

from services.messaging.email_service import send_bulk_email
from warehouse.models import LocationRequest, ResponseModel, SendBulkEmailData, SendEmailData
from warehouse.warehouse_service import fetch_orders_by_requestid_from_airtable, fetch_orders_from_airtable, fetch_warehouses_from_airtable, find_nearby_warehouses


warehouse_router = APIRouter()


@warehouse_router.get("/warehouses")
async def warehouses():
    try:
        data = await fetch_warehouses_from_airtable()
        return ResponseModel(status="success", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@warehouse_router.get("/requests")
async def requests(request_id: int):
    try:
        data = await fetch_orders_by_requestid_from_airtable(request_id=request_id)
        if not data:
            raise HTTPException(status_code=404, detail=f"Order with Request ID {request_id} not found")
        return ResponseModel(status="success", data=data)   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@warehouse_router.get("/all-requests")
async def requests():
    try:
        data = await fetch_orders_from_airtable()
        if not data:
            raise HTTPException(status_code=404, detail=f"Orders not found")
        return ResponseModel(status="success", data=data)   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@warehouse_router.post("/nearby_warehouses")
async def find_nearby_warehouses_endpoint(request: LocationRequest):
    try:
        nearby_warehouses = await find_nearby_warehouses(request.zip_code, request.radius_miles)
        encoded = jsonable_encoder(nearby_warehouses, exclude_none=False)
        return ResponseModel(status="success", data=encoded)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@warehouse_router.post("/send_email")
async def send_bulk_email_endpoint(send_bulk_emails: SendBulkEmailData):
    try:
        response = await send_bulk_email(send_bulk_emails)
        return ResponseModel(status="success", data=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")