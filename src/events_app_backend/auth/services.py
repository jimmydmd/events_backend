from fastapi import HTTPException, status
from sqlmodel import Session
from events_app_backend.users.models import User
from events_app_backend.core.security import hash_password, verify_password, create_access_token
from .repositories import get_user_by_email, get_participant_role, create_user

def register_user(db: Session, user_data):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    participant_role = get_participant_role(db)
    role_id = participant_role.id if participant_role else None

    new_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=hash_password(user_data.password),
        role_id=role_id
    )
    return create_user(db, new_user)

def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    role_name = user.role.name if user.role else "Participant"

    token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "role": role_name, 
        "first_name": user.first_name,
        "last_name": user.last_name
    })
    return token
