import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from events_app_backend.core.models import SoftDeleteMixin

if TYPE_CHECKING:
    from events_app_backend.users.models import User
    from events_app_backend.registrations.models import EventRegistration

class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Event(SoftDeleteMixin, SQLModel, table=True):
    __tablename__ = "events"

    id: Optional[uuid.UUID] = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int
    created_by: uuid.UUID = Field(foreign_key="users.id")  
    status: EventStatus = Field(
        sa_column=Column(SAEnum(EventStatus, name="event_status_enum"), nullable=False, default=EventStatus.DRAFT)
    )
    creator: Optional["User"] = Relationship(back_populates="created_events")
    registrations: List["EventRegistration"] = Relationship(back_populates="event")
    sessions: list["Session"] = Relationship(back_populates="event")


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: Optional[uuid.UUID] = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    event_id: uuid.UUID = Field(foreign_key="events.id")
    title: str
    description: Optional[str] = None
    speaker: str
    start_time: datetime
    end_time: datetime
    capacity: Optional[int] = None  

    event: Optional["Event"] = Relationship(back_populates="sessions")
    @property
    def event_name(self) -> Optional[str]:
        return self.event.name if self.event else None