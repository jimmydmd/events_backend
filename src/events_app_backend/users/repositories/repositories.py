from sqlmodel import Session, select
from typing import List, Optional
from events_app_backend.users.models import User

def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.get(User, user_id)

def list_users(db: Session) -> List[User]:
    return db.exec(select(User)).all()

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_data(db: Session, user: User, update_data: dict) -> User:
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

