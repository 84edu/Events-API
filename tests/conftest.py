import pytest
import requests
import time


@pytest.fixture
def base_url():
    """Provides the base URL for the API tests."""
    return "http://localhost:5002"


@pytest.fixture
def auth_token(base_url):
    """
    Registers a test user, logs them in, and returns the JWT token.
    Required for authenticated requests.
    """
    # Unique username via timestamp (prevents 'User exists' errors)
    unique_user = f"testuser_{int(time.time())}"
    password = "testpassword123"

    # 1. Registering
    requests.post(f"{base_url}/api/auth/register", json={
        "username": unique_user,
        "password": password
    })

    # 2. Login
    login_res = requests.post(f"{base_url}/api/auth/login", json={
        "username": unique_user,
        "password": password
    })

    # Extract the token from the response (Assumption: The key is named 'access_token').
    return login_res.json().get("access_token")
