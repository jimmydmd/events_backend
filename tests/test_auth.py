import pytest
from src.events_app_backend.core.test_database import TestUser, TestRole, get_session

@pytest.fixture
def session():
    with get_session() as s:
        yield s

def test_user_creation(session):
    # Crear rol
    role = TestRole(name="Admin")
    session.add(role)
    session.commit()
    session.refresh(role)

    # Crear usuario
    user = TestUser(username="jmartinez", email="jmartinez@test.com", role_id=role.id)
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.role_id == role.id
    assert user.username == "jmartinez"
