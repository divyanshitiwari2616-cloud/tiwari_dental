from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppointmentCreate(BaseModel):

    name: str
    phone: str
    service: str
    location: str
    message: Optional[str] = None


class AppointmentStatusUpdate(BaseModel):

    status: str


class AppointmentResponse(AppointmentCreate):

    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True