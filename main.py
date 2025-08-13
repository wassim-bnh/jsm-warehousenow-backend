from contextlib import asynccontextmanager
from fastapi import FastAPI
import requests
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from geolocation.route import geolocation_router
from jsm_warehouse.jsm_warehouse_service import cache_warehouses
from jsm_warehouse.route import warehouse_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #await cache_warehouses()
    print("Caching..")
    yield
    print("App is shutting down...")


app = FastAPI(title="jsm-warehousenow", lifespan=lifespan)


app.include_router(geolocation_router, prefix="/geolocation")
app.include_router(warehouse_router, )
