from fastapi import APIRouter, Depends
from sqlmodel import Session
from events_app_backend.core.database import get_session
from events_app_backend.core.security import get_current_user
from events_app_backend.registrations.schemas import EventRegistrationCreate, EventRegistrationRead, UserEventRead
from events_app_backend.registrations.services.services import (
    register_user_to_event_service,
    list_user_registrations_service
)
from events_app_backend.core.permissions import require_role

router = APIRouter()

@router.post("/", response_model=EventRegistrationRead)
def register_user_to_event(
        registration_data: EventRegistrationCreate,
        db: Session = Depends(get_session),
        current_user = Depends(require_role("Participant"))
    ):
    return register_user_to_event_service(db, registration_data.event_id, current_user.id)

# Solo el propio usuario puede ver sus registros
@router.get("/my_registrations", response_model=list[UserEventRead])
def get_my_registrations(
        db: Session = Depends(get_session),
        current_user = Depends(require_role("Participant"))
    ):
    return list_user_registrations_service(db, current_user.id)
