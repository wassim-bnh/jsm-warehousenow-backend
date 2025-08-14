
from openai import BaseModel
from typing import List, Generic, TypeVar
from pydantic.generics import GenericModel

class LocationRequest(BaseModel):
    zip_code: str
    radius_miles: float = 50 


class Warehouse(BaseModel):
    id: str
    name: str
    zip: int
    city: str
    state: str

T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    status: str
    data: T