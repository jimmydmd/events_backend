from sqlmodel import Session, select
from uuid import UUID
from events_app_backend.events.models import Event
from events_app_backend.registrations.models import EventRegistration
from sqlalchemy import func


def get_event(db: Session, event_id: UUID) -> Event | None:
    return db.exec(
        select(Event).where(Event.id == event_id, Event.is_deleted == False)
    ).first()


def count_event_registrations(db: Session, event_id: UUID) -> int:
    return db.exec(
        select(func.count()).select_from(EventRegistration).where(EventRegistration.event_id == event_id)
    ).one()


def get_registration(db: Session, event_id: UUID, user_id: UUID) -> EventRegistration | None:
    return db.exec(
        select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id
        )
    ).first()


def create_registration(db: Session, user_id: UUID, event_id: UUID) -> EventRegistration:
    registration = EventRegistration(user_id=user_id, event_id=event_id)
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration


def list_user_registrations(db: Session, user_id: UUID):
    # Solo traer eventos que no estén soft deleted
    return db.exec(
        select(EventRegistration, Event)
        .join(Event, Event.id == EventRegistration.event_id)
        .where(EventRegistration.user_id == user_id, Event.is_deleted == False)
    ).all()
