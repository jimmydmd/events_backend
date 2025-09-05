import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

if TYPE_CHECKING:
    from events_app_backend.roles.models import Role
    from events_app_backend.events.models import Event
    from events_app_backend.registrations.models import EventRegistration


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True, nullable=False)
    password: str
    role_id: Optional[uuid.UUID] = Field(default=None, foreign_key="roles.id")


    role: Optional["Role"] = Relationship(back_populates="users")
    created_events: List["Event"] = Relationship(back_populates="creator")
    registrations: List["EventRegistration"] = Relationship(back_populates="user")

    @property
    def role_name(self) -> Optional[str]:
        return self.role.name if self.role else None