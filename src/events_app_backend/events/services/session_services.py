from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session
from typing import Optional
from events_app_backend.events.models import Event, Session as SessionModel
from events_app_backend.events.repositories.session_repositories import (
    get_session_by_id, list_sessions, create_session, update_session_data, delete_session
)
from events_app_backend.events.services.event_services import validate_total_capacity
from events_app_backend.events.models import EventStatus

def ensure_event_published(event: Event):
    if event.status != EventStatus.PUBLISHED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot modify sessions of an event with status {event.status.name}"
        )

def list_sessions_service(db: Session, event_id: Optional[UUID]):
    return list_sessions(db, event_id)

def create_session_service(db: Session, data, current_user_id: UUID):
    event = db.get(Event, data.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    ensure_event_published(event)

    if data.start_time < event.start_date or data.end_time > event.end_date:
        raise HTTPException(status_code=400, detail="Session must be within the event's date range")

    validate_total_capacity(db, data.event_id, data.capacity)

    new_session = SessionModel(**data.model_dump())
    return create_session(db, new_session)

def update_session_service(db: Session, session_id: UUID, data):
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    ensure_event_published(session_obj.event)

    if data.start_time and data.end_time:
        if data.start_time < session_obj.event.start_date or data.end_time > session_obj.event.end_date:
            raise HTTPException(status_code=400, detail="Session must be within the event's date range")

    if data.capacity is not None:
        validate_total_capacity(db, session_obj.event_id, data.capacity, exclude_session_id=session_id)

    return update_session_data(db, session_obj, data.model_dump(exclude_unset=True))

def delete_session_service(db: Session, session_id: UUID):
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    ensure_event_published(session_obj.event)

    delete_session(db, session_obj)
    return {"detail": "Session deleted successfully"}
