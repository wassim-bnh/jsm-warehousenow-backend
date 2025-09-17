
from typing import List, Generic, TypeVar
from pydantic import BaseModel

class LocationRequest(BaseModel):
    zip_code: str
    radius_miles: float = 50 


from typing import List, Optional
from pydantic import BaseModel

class WarehouseFields(BaseModel):
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[int] = None
    Name: Optional[str] = None
    Full_Address: Optional[List[str]] = None
    Status: Optional[str] = None
    Tier: Optional[str] = None
    Contact_1: Optional[str] = None
    Email_1: Optional[str] = None
    Office_number: Optional[str] = None
    Cell_number_1: Optional[str] = None
    Contact_2: Optional[str] = None
    Cell_number_2: Optional[str] = None
    Email_2: Optional[str] = None
    Email_3: Optional[str] = None
    Hours: Optional[str] = None
    Hazmat: Optional[str] = None
    Temp_Control: Optional[str] = None
    Food_Grade: Optional[str] = None
    Paper_Rolls: Optional[str] = None
    Services: Optional[List[str]] = None
    Website: Optional[str] = None
    Notes_Pricing: Optional[str] = None
    Insurance: Optional[str] = None
    createdTime: str = None

class WarehouseData(BaseModel):
    id: str
    fields: WarehouseFields

class FilterWarehouseData(BaseModel):
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[int] = None
    Status: Optional[str] = None
    Tier: Optional[str] = None
    Hazmat: Optional[str] = None
    Temp_Control: Optional[str] = None
    Food_Grade: Optional[str] = None
    Paper_Rolls: Optional[str] = None
    Services: Optional[List[str]] = None
    Notes_Pricing: Optional[str] = None
    Insurance: Optional[str] = None

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    status: str
    data: T

class SendEmailData(BaseModel):
    email: str
    services: list[str]
    adress: str

class SendBulkEmailData(BaseModel):
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    emails_data: list[SendEmailData]
    images: list[str] = None