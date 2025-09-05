import uuid
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Optional
from events_app_backend.events.models import Event, EventStatus, Session as SessionModel
from events_app_backend.events.schemas import (
    EventCreate,
    EventRead,
    EventUpdate,
    SessionCreate,
    SessionRead,
)
from events_app_backend.core.database import get_session
from events_app_backend.core.security import get_current_user
from events_app_backend.events.services.event_services import (
    cancel_event_service,
    create_event_service,
    delete_event_service,
    list_events_service,
    update_event_service,
)
from events_app_backend.events.services.session_services import create_session_service, delete_session_service, list_sessions_service, update_session_service
from events_app_backend.core.permissions import require_role

router = APIRouter()

# TODO: Verificar permisos del usuario actual

@router.post("/", response_model=EventRead)
def create_event(
    event_data: EventCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("Admin", "Organizer")),
):
    return create_event_service(session, event_data, current_user.id)


@router.get("/", response_model=List[EventRead])
def list_events(
        term: Optional[str] = Query(None),
        limit: int = 20,
        offset: int = 0,
        session: Session = Depends(get_session),
        current_user=Depends(require_role("Admin", "Organizer", "Participant")),
    ):
    return list_events_service(session, term, limit, offset)


@router.patch("/{event_id}", response_model=EventRead)
def update_event(
        event_id: uuid.UUID = Path(...),
        event_data: EventUpdate = None,
        session: Session = Depends(get_session),
        current_user=Depends(require_role("Admin", "Organizer")),
    ):
    return update_event_service(session, event_id, event_data.model_dump(exclude_unset=True))


@router.delete("/{event_id}")
def delete_event(
        event_id: uuid.UUID,
        session: Session = Depends(get_session),
        current_user=Depends(require_role("Admin")),
    ):
    return delete_event_service(session, event_id)


@router.patch("/{event_id}/cancel", response_model=EventRead)
def cancel_event(
        event_id: uuid.UUID,
        session: Session = Depends(get_session),
        current_user=Depends(require_role("Admin", "Organizer")),
    ):
    return cancel_event_service(session, event_id)

# Session Endpoints

@router.get("/sessions/", response_model=List[SessionRead])
def list_sessions_route(
        event_id: Optional[uuid.UUID] = None,
        db: Session = Depends(get_session),
        current_user=Depends(require_role("Admin", "Organizer", "Participant")),
    ):
    return list_sessions_service(db, event_id)


@router.post("/sessions/", response_model=SessionRead)
def create_session_route(
        session_data: SessionCreate,
        db: Session = Depends(get_session),
        current_user=Depends(require_role("Admin", "Organizer")),
    ):
    return create_session_service(db, session_data, current_user.id)


@router.patch("/sessions/{session_id}", response_model=SessionRead)
def update_session_route(
        session_id: uuid.UUID,
        session_data: SessionCreate,
        db: Session = Depends(get_session),
        current_user=Depends(require_role("Admin", "Organizer")),
    ):
    return update_session_service(db, session_id, session_data)


@router.delete("/sessions/{session_id}")
def delete_session_route(
        session_id: uuid.UUID,
        db: Session = Depends(get_session),
        current_user=Depends(require_role("Admin")),
    ):
    return delete_session_service(db, session_id)