import uuid
import pytest
from src.events_app_backend.core.test_database import TestEvent, TestSession, get_session

@pytest.fixture
def session():
    with get_session() as s:
        yield s

def test_create_event_and_session(session):
    event = TestEvent(name="Evento de prueba", capacity=100)
    session.add(event)
    session.commit()
    session.refresh(event)

    session_model = TestSession(
        event_id=event.id,
        title="Sesión 1",
        speaker="Ponente Test",
        capacity=50
    )
    session.add(session_model)
    session.commit()
    session.refresh(session_model)

    assert event.id is not None
    assert session_model.id is not None
    assert session_model.event_id == event.id
