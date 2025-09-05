from fastapi import Depends, HTTPException, status
from events_app_backend.users.models import User
from events_app_backend.core.security import get_current_user

def require_role(*allowed_roles: str):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return current_user
    return dependency
