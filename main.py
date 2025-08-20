from contextlib import asynccontextmanager
from fastapi import FastAPI
from warehouse.warehouse_route import warehouse_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #await cache_warehouses()
    print("Caching..")
    yield
    print("App is shutting down...")


app = FastAPI(title="jsm-warehousenow", lifespan=lifespan)


app.include_router(warehouse_router)
