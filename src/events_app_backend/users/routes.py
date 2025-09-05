from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from events_app_backend.core.database import get_session
from events_app_backend.core.security import get_current_user
from events_app_backend.core.permissions import require_role
from events_app_backend.users.models import User
from events_app_backend.users.schemas import UserRead, UserUpdate, UserCreate
from events_app_backend.users.services.services import (
    create_user_service,
    list_users_service,
    update_user_service,
    delete_user_service,
    get_user_service
)

router = APIRouter(tags=["Users"]) 

@router.get("/", response_model=List[UserRead])
def list_users(
        session: Session = Depends(get_session),
        current_user = Depends(require_role("Admin"))
    ):
    return list_users_service(session)

@router.post("/", response_model=UserRead)
def create_user(
        user_data: UserCreate,
        session: Session = Depends(get_session),
        current_user = Depends(require_role("Admin"))
    ):
    return create_user_service(session, user_data)

@router.get("/{user_id}", response_model=UserRead)
def get_user(
        user_id: str,
        session: Session = Depends(get_session),
        current_user = Depends(require_role("Admin"))
    ):
    return get_user_service(session, user_id)

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
        user_id: str,
        user_data: UserUpdate,
        session: Session = Depends(get_session),
        current_user = Depends(require_role("Admin"))
    ):
    return update_user_service(session, user_id, user_data)

@router.delete("/{user_id}")
def delete_user(
        user_id: str,
        session: Session = Depends(get_session),
        current_user = Depends(require_role("Admin"))
    ):
    return delete_user_service(session, user_id)
