from sqlmodel import Session, select
from typing import List, Optional
from events_app_backend.events.models import Event, Session as SessionModel
from sqlalchemy.orm import selectinload

def get_event(db: Session, event_id: str) -> Optional[Event]:

    return db.get(Event, event_id)

def list_events(db: Session, term: Optional[str], limit: int, offset: int) -> List[Event]:
    query = select(Event).where(Event.is_deleted == False).options(
        selectinload(Event.sessions)  
    ) 
    if term:
        query = query.where(Event.name.ilike(f"%{term}%") | Event.description.ilike(f"%{term}%"))
    return db.exec(query.offset(offset).limit(limit)).all()

def create_event(db: Session, event: Event) -> Event:
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event_data(db: Session, event: Event, update_data: dict) -> Event:
    for key, value in update_data.items():
        setattr(event, key, value)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def soft_delete_event(db: Session, event: Event) -> Event:
    event.is_deleted = True
    db.add(event)
    db.commit()
    return {"detail": "Event deleted successfully"}

def cancel_event(db: Session, event: Event) -> Event:
    event.status = "cancelled"
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
