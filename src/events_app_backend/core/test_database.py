import os
import uuid
from typing import Optional
import pytest
from sqlmodel import SQLModel, Field, create_engine, Session

SQLModel.metadata.clear()

TEST_DB_FILE = "test.db"
if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

class TestRole(SQLModel, table=True):
    __tablename__ = "test_roles"
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str

class TestUser(SQLModel, table=True):
    __tablename__ = "test_user"
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    role_id: Optional[uuid.UUID] = Field(default=None, foreign_key="roles.id")


class TestEvent(SQLModel, table=True):
    __tablename__ = "test_events"
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    capacity: int = 0
    created_by: Optional[uuid.UUID] = None
    status: str = "DRAFT"
    is_deleted: bool = False


class TestSession(SQLModel, table=True):
    __tablename__ = "test_sessions"
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_id: uuid.UUID
    title: str
    description: Optional[str] = None
    speaker: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    capacity: Optional[int] = 0

def init_db():
    engine = create_engine(f"sqlite:///{TEST_DB_FILE}", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine

def get_session():
    engine = init_db()
    return Session(engine)
