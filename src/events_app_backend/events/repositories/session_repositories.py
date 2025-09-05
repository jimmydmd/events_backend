from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from events_app_backend.events.models import Session as SessionModel

def get_session_by_id(db: Session, session_id: UUID) -> Optional[SessionModel]:
    return db.get(SessionModel, session_id)

def list_sessions(db: Session, event_id: Optional[UUID] = None) -> List[SessionModel]:
    stmt = select(SessionModel)
    if event_id:
        stmt = stmt.where(SessionModel.event_id == event_id)
    return db.exec(stmt).all()

def create_session(db: Session, session_obj: SessionModel) -> SessionModel:
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj

def update_session_data(db: Session, session_obj: SessionModel, update_data: dict) -> SessionModel:
    for key, value in update_data.items():
        setattr(session_obj, key, value)
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj

def delete_session(db: Session, session_obj: SessionModel) -> None:
    db.delete(session_obj)
    db.commit()
