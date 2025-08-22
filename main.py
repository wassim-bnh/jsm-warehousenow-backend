from contextlib import asynccontextmanager
from fastapi import FastAPI
from warehouse.warehouse_route import warehouse_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    #await cache_warehouses()
    print("Caching..")
    yield
    print("App is shutting down...")
    

app = FastAPI(title="jsm-warehousenow", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- This allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(warehouse_router)
