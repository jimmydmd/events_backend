from sqlmodel import Session, select
from fastapi import HTTPException
from sqlmodel import Session
from events_app_backend.users.models import User
from events_app_backend.users.repositories.repositories import (
    get_user, list_users, create_user, update_user_data
)
from events_app_backend.core.security import hash_password

def list_users_service(db: Session):
    return list_users(db)

def get_user_service(db: Session, user_id: str):
    user = get_user(db, user_id)
    if not user :
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user_service(db: Session, user_data):
    existing_user = db.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data.password = hash_password(user_data.password)
    new_user = User(**user_data.dict())
    return create_user(db, new_user)

def update_user_service(db: Session, user_id: str, data):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Si se intenta cambiar el email, verificar duplicados
    new_email = data.email if hasattr(data, "email") else None
    if new_email and new_email != user.email:
        existing_user = db.exec(select(User).where(User.email == new_email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")

    # Actualizar campos
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user_service(db: Session, user_id: str):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
