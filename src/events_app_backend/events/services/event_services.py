from datetime import datetime
import uuid
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Optional
from events_app_backend.events.models import Event, EventStatus, Session as SessionModel
from events_app_backend.utils.datetime_utils import normalize_event_dates
from sqlalchemy import func
from events_app_backend.events.repositories.event_repositories import get_event, update_event_data, soft_delete_event, create_event, list_events


def validate_total_capacity(db: Session, event_id: uuid.UUID, new_capacity: int, exclude_session_id: Optional[uuid.UUID] = None):
    query = db.query(func.sum(SessionModel.capacity)).filter(SessionModel.event_id == event_id)
    
    if exclude_session_id:
        query = query.filter(SessionModel.id != exclude_session_id)

    current_capacity = query.scalar() or 0
    event = db.get(Event, event_id)
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_capacity + (new_capacity or 0) > event.capacity:
        raise HTTPException(
            status_code=400,
            detail=f"The total capacity of all sessions ({current_capacity + (new_capacity or 0)}) cannot exceed the event capacity ({event.capacity})"
        )

def create_event_service(db: Session, data, user_id: str) -> Event:
    start, end = normalize_event_dates(data.start_date, data.end_date)

    now = datetime.now()
    if start < now:
        raise HTTPException(status_code=400, detail="Start date cannot be in the past")
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    event = Event(**data.dict(), created_by=user_id)

    return create_event(db, event)

def list_events_service(db: Session, term: Optional[str], limit: int, offset: int) -> List[Event]:
    return list_events(db, term, limit, offset)

def update_event_service(db: Session, event_id: UUID, update_data: dict):
    event = get_event(db, event_id)
    
    if not event or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")

    start = update_data.get("start_date", event.start_date)
    end = update_data.get("end_date", event.end_date)

    start, end = normalize_event_dates(start, end)

    now = datetime.now()
    
    if start < now:
        raise HTTPException(status_code=400, detail="Start date cannot be in the past")
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    update_data["start_date"] = start
    update_data["end_date"] = end

    return update_event_data(db, event, update_data)

def delete_event_service(db: Session, event_id: UUID):
    event = get_event(db, event_id)

    if not event or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return soft_delete_event(db, event)

def cancel_event_service(db: Session, event_id: UUID):
    event = get_event(db, event_id)

    if not event or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.status == EventStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Event is already cancelled")

    event.status = EventStatus.CANCELLED
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return event