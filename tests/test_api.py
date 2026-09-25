def test_home_returns_successful_response(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Student Management API is working!"


def test_user_registration_works(client):
    import uuid

    credentials = {
        "username": f"registration-{uuid.uuid4().hex}",
        "password": f"test-password-{uuid.uuid4().hex}",
    }

    response = client.post("/auth/register", json=credentials)

    assert response.status_code == 200
    assert response.json() == {
        "message": "User registered successfully",
        "username": credentials["username"],
    }


def test_login_returns_access_token(client, registered_user):
    response = client.post("/auth/login", json=registered_user)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
