from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Optional
from events_app_backend.core.database import get_session
from events_app_backend.core.security import get_current_user
from events_app_backend.users.schemas import UserCreate, UserLogin, UserRead, TokenResponse
from .services import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session),
             current_user: Optional[UserRead] = Depends(lambda: get_current_user(optional=True))):
    return register_user(session, user_data)

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    token = login_user(session, credentials.email, credentials.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", response_model=UserRead)
def profile(current_user: UserRead = Depends(get_current_user)):
    return current_user
