from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional
from datetime import datetime
from fastapi import UploadFile, File


class Advertisement(BaseModel):
    title:str = Field(..., max_length=100, description="Title of the advertisement")
    decription: Optional[str] = Field(..., max_lenght=1000, description="Description of the advertisement")
    price: float = Field(..., ge=0, description="Price of the product or service")
    created_at: datetime = Field(datetime.now(), description="Date of the creation")
    photo: UploadFile = File(...)

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