from datetime import datetime
from models import User, Event


def test_check_password():
    test_user = User(username="user1")
    raw_password = "securepassword123"
    test_user.set_password(raw_password)

    assert test_user.password_hash is not None
    assert test_user.password_hash != raw_password
    assert test_user.check_password(raw_password) is True
    assert test_user.check_password("wrong_pass") is False


def test_event_to_dict():
    """Tests the conversion of an event into a dictionary."""

    mock_date = datetime(2026, 5, 20, 10, 0)

    new_event = Event(
        id=99,
        title="Unit Test Workshop",
        description="Testen ohne DB",
        date=mock_date,
        location="Home Office",
        capacity=10,
        created_by=1
    )

    event_data = new_event.to_dict()

    assert event_data['title'] == "Unit Test Workshop"
    assert event_data['location'] == "Home Office"
    assert "2026-05-20T10:00:00" in event_data['date']
    assert event_data['rsvp_count'] == 0
