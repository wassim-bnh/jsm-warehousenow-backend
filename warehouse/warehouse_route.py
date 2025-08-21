from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
import httpx
import requests

from services.messaging.email_service import send_bulk_email
from warehouse.models import LocationRequest, ResponseModel, SendEmailData
from warehouse.warehouse_service import fetch_warehouses_from_airtable, find_nearby_warehouses


warehouse_router = APIRouter()


@warehouse_router.get("/warehouses")
async def warehouses():
    try:
        data = await fetch_warehouses_from_airtable()
        return ResponseModel(status="success", data=data)
    except (httpx.HTTPError, requests.exceptions.RequestException) as e:
        raise HTTPException(status_code=502, detail=f"Error fetching warehouses: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@warehouse_router.post("/nearby_warehouses")
async def find_nearby_warehouses_endpoint(request: LocationRequest):
    try:
        nearby_warehouses = await find_nearby_warehouses(request.zip_code, request.radius_miles)
        encoded = jsonable_encoder(nearby_warehouses, exclude_none=False)
        return ResponseModel(status="success", data=encoded)
    except (httpx.HTTPError, requests.exceptions.RequestException) as e:
        raise HTTPException(status_code=502, detail=f"Error fetching nearby warehouses: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@warehouse_router.post("/send_email")
async def send_bulk_email_endpoint(emails_data: list[SendEmailData]):
    try:
        response = await send_bulk_email(emails_data)
        return ResponseModel(status="success", data=response)
    except (httpx.HTTPError, requests.exceptions.RequestException) as e:
        raise HTTPException(status_code=502, detail=f"Error sending emails: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")