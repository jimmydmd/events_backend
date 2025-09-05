from events_app_backend.core.permissions import require_role
from events_app_backend.roles.models import Role
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from events_app_backend.core.database import get_session


router = APIRouter(tags=["Roles"])

@router.get("/", response_model=list[Role])
def list_roles(session: Session = Depends(get_session), current_user=Depends(require_role("Admin"))):
    roles = session.exec(select(Role)).all()
    return roles
