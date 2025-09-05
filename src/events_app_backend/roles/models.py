import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from events_app_backend.users.models import User


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[uuid.UUID] = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str  
    description: Optional[str] = None

    users: List["User"] = Relationship(back_populates="role")
