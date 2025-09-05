import pytest
from src.events_app_backend.core.test_database import get_session
from src.events_app_backend.users.services.services import (
    create_user_service,
    list_users_service,
    update_user_service,
    delete_user_service,
)
from pydantic import BaseModel

# Modelo simplificado para tests
class UserCreateMock(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role_id: str | None = None

class UserUpdateMock(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    role_id: str | None = None

@pytest.fixture
def session():
    with get_session() as s:
        yield s

def test_create_and_list_user(session):
    # Crear usuario
    user_data = UserCreateMock(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="secret"
    )
    user = create_user_service(session, user_data)
    assert user.id is not None
    assert user.email == "test@example.com"

    # Listar usuarios
    users = list_users_service(session)
    assert len(users) == 1
    assert users[0].email == "test@example.com"

def test_update_user(session):
    # Crear usuario inicial
    user_data = UserCreateMock(
        first_name="Update",
        last_name="User",
        email="update@example.com",
        password="secret"
    )
    user = create_user_service(session, user_data)

    # ⚡ Pasar UUID directamente
    update_data = UserUpdateMock(first_name="Updated")
    updated_user = update_user_service(session, user.id, update_data)
    assert updated_user.first_name == "Updated"

def test_delete_user(session):
    # Crear usuario
    user_data = UserCreateMock(
        first_name="Delete",
        last_name="User",
        email="delete@example.com",
        password="secret"
    )
    user = create_user_service(session, user_data)

    # ⚡ Pasar UUID directamente
    response = delete_user_service(session, user.id)
    assert response["detail"] == "User deleted successfully"

    # Verificar que no existe
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        delete_user_service(session, user.id)
