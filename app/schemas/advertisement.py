from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Annotated
from datetime import datetime
from fastapi import UploadFile, File


from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class Advertisement(BaseModel):
    title: str = Field(..., max_length=100, description="Title of the advertisement")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the advertisement")
    price: float = Field(..., ge=0, description="Price of the product or service")
    category: str = Field(..., min_length=3, max_length=30, description="Category of the product")
    published_at: datetime = Field(default_factory=datetime.now, description="Date of the creation")
    photo: Annotated[UploadFile, File(...)] = None

    @field_validator("created_at")
    @classmethod
    def check_date(cls,value):
        if value < datetime.now():
            raise ValueError("Date cannot be in the past")
        return value
    
    
    @field_validator("price")
    @classmethod
    def check_price(cls,value):
        if value < 0:
            raise ValueError("The price must be higher then 0")
        return value
    


class UpdateItemSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=3, max_length=30)



class ItemResponse(BaseModel):
    id: int
    title: str
    category: str
    price: float
    published_at: datetime