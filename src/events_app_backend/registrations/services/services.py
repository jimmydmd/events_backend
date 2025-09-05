from fastapi import HTTPException
from sqlmodel import Session
from events_app_backend.registrations.repositories.repositories import (
    get_event, count_event_registrations, get_registration, create_registration, list_user_registrations
)
from events_app_backend.events.models import EventStatus


def register_user_to_event_service(db: Session, event_id, user_id):
    event = get_event(db, event_id)
    if not event or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.status != EventStatus.PUBLISHED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot register for event with status '{event.status.name}'"
        )

    if count_event_registrations(db, event_id) >= event.capacity:
        raise HTTPException(status_code=400, detail="The event is at full capacity")

    if get_registration(db, event_id, user_id):
        raise HTTPException(status_code=400, detail="User is already registered for this event")

    return create_registration(db, user_id, event_id)

def list_user_registrations_service(db: Session, user_id):
    registrations = list_user_registrations(db, user_id)
    result = []
    for registration, event in registrations:
        result.append({
            "event_id": event.id,
            "name": event.name,
            "start_date": event.start_date,
            "end_date": event.end_date,
            "capacity": event.capacity,
            "registered_at": registration.registered_at
        })
    return result
