from events_app_backend.events.models import EventStatus
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import  List, Optional
import uuid

class SessionRead(BaseModel):
    id: uuid.UUID
    event_id: uuid.UUID
    title: str
    description: Optional[str]
    speaker : str
    start_time: datetime
    end_time: datetime
    capacity: Optional[int]
    event_name: Optional[str] = None  
    class Config:
        from_attributes = True 

class SessionCreate(BaseModel):
    event_id: uuid.UUID
    title: str
    description: Optional[str]
    speaker: str  
    start_time: datetime
    end_time: datetime
    capacity: Optional[int]

    @validator("end_time")
    def check_time(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be greater than start_time")
        return v
    
    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int = Field(..., gt=0) 
    status: Optional[EventStatus] = EventStatus.DRAFT

class EventRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    capacity: int
    created_by: Optional[uuid.UUID]
    created_at: datetime
    status: EventStatus
    sessions: List[SessionRead] = []  

    class Config:
        orm_mode = True


class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    capacity: Optional[int] = Field(None, gt=0)
    status: Optional[EventStatus] = None


