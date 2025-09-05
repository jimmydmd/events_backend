import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


if TYPE_CHECKING:
    from events_app_backend.users.models import User
    from events_app_backend.events.models import Event
class EventRegistration(SQLModel, table=True):
    __tablename__ = "event_registrations"

    id: Optional[uuid.UUID] = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(foreign_key="users.id")  
    event_id: uuid.UUID = Field(foreign_key="events.id")
    registered_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="registrations")
    event: Optional["Event"] = Relationship(back_populates="registrations")
