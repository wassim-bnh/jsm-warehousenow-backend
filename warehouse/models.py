
from openai import BaseModel
from typing import List, Generic, TypeVar
from pydantic.generics import GenericModel

class LocationRequest(BaseModel):
    zip_code: str
    radius_miles: float = 50 


from typing import List, Optional
from pydantic import BaseModel

class WarehouseFields(BaseModel):
    City: Optional[str]
    State: Optional[str]
    Zip: Optional[int]
    Name: Optional[str]
    Full_Address: Optional[List[str]] 
    Status: Optional[str]
    Tier: Optional[str]
    Contact_1: Optional[str]
    Email_1: Optional[str]
    Office_number: Optional[str]
    Cell_number_1: Optional[str]
    Contact_2: Optional[str]
    Cell_number_2: Optional[str]
    Email_2: Optional[str]
    Email_3: Optional[str]
    Hours: Optional[str]
    Hazmat: Optional[str]
    Temp_Control: Optional[str]
    Food_Grade: Optional[str]
    Paper_Rolls: Optional[str]
    Services: Optional[List[str]]
    Website: Optional[str]
    Notes_Pricing: Optional[str]
    Insurance: Optional[str]
    createdTime: str

class WarehouseData(BaseModel):
    id: str
    fields: WarehouseFields


T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    status: str
    data: T