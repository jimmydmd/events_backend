from sqlmodel import Session, select
from events_app_backend.users.models import User
from events_app_backend.roles.models import Role
from sqlalchemy.orm import joinedload

def get_user_by_email(db: Session, email: str):
    return db.exec(
        select(User)
        .where(User.email == email)
        .options(joinedload(User.role))  # ¡Esta línea carga la relación!
    ).first()

def get_participant_role(db: Session):
    return db.exec(select(Role).where(Role.name == "Participant")).first()

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

