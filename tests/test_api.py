import requests
import time


def test_health_endpoint_returns_healthy(base_url):
    """
    Test 1: Checks the health check endpoint.
    Requirement: Status 200 and JSON confirmation.
    """
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200

    assert response.json().get("status") == "healthy"


def test_register_user_creates_new_user(base_url):
    """
    Test 2: User Registration.
    Requirement: Status 201 and return of the username.
    """
    unique_username = f"user_{int(time.time())}"
    payload = {
        "username": unique_username,
        "password": "securepassword123"
    }
    response = requests.post(f"{base_url}/register", json=payload)

    assert response.status_code == 201
    assert response.json().get("username") == unique_username


def test_login_returns_jwt_token(base_url):
    """
    Test 3: User Login.
    Requirement: Status 200 and receipt of a token.
    """
    username = f"login_user_{int(time.time())}"
    password = "password123"
    requests.post(f"{base_url}/register", json={"username": username, "password": password})

    # The login test
    payload = {"username": username, "password": password}
    response = requests.post(f"{base_url}/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_public_event_requires_auth_and_succeeds_with_token(base_url, auth_token):
    """
    Test 4: Create event (authenticated).
    Uses the 'auth_token' fixture from conftest.py.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Integration Test Event",
        "description": "Erstellt via automatisierter Testsuite",
        "date": "2026-06-01T18:00:00",
        "location": "Test Center",
        "capacity": 50,
        "is_public": True
    }

    response = requests.post(f"{base_url}/events", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json().get("title") == "Integration Test Event"


def test_rsvp_to_public_event(base_url, auth_token):
    """
    Test 5: Event Registration (RSVP)
    """
    # 1. First, create an event that people can sign up for.
    headers = {"Authorization": f"Bearer {auth_token}"}
    event_payload = {
        "title": "RSVP Test Event",
        "date": "2026-07-01T12:00:00",
        "is_public": True
    }
    event_res = requests.post(f"{base_url}/events", json=event_payload, headers=headers)
    event_id = event_res.json().get("id")

    # 2. Send RSVP
    rsvp_payload = {"attending": True}
    response = requests.post(f"{base_url}/events/{event_id}/rsvp", json=rsvp_payload, headers=headers)

    assert response.status_code == 201 or response.status_code == 200
    assert response.json().get("message") is not None
