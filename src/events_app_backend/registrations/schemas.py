from pydantic import BaseModel
import uuid
from datetime import datetime


class EventRegistrationCreate(BaseModel):
    event_id: uuid.UUID


class EventRegistrationRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    event_id: uuid.UUID
    registered_at: datetime

    class Config:
        from_attributes = True

class UserEventRead(BaseModel):
    event_id: uuid.UUID
    name: str
    start_date: datetime
    end_date: datetime
    capacity: int
    registered_at: datetime
    
    class Config:
        orm_mode = True