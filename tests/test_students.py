import uuid

import pytest


def student_payload(**overrides):
    payload = {
        "id": uuid.uuid4().int % 2_000_000_000 + 1,
        "name": f"Student {uuid.uuid4().hex[:8]}",
        "age": 20,
        "course": "Computer Science",
    }
    payload.update(overrides)
    return payload


def create_student(client, **overrides):
    response = client.post("/students/", json=student_payload(**overrides))
    assert response.status_code == 200, response.text
    return response.json()["student"]


def test_authenticated_user_can_list_students(authenticated_client):
    student = create_student(authenticated_client)

    response = authenticated_client.get("/students/")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [student["id"]]


def test_authenticated_user_can_create_get_update_and_delete_student(
    authenticated_client,
):
    payload = student_payload()

    created = authenticated_client.post("/students/", json=payload)
    assert created.status_code == 200
    student_id = created.json()["student"]["id"]

    fetched = authenticated_client.get(f"/students/{student_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == payload["name"]

    updated_payload = student_payload(
        id=student_id,
        name="Updated Student",
        course="Updated Course",
    )
    updated = authenticated_client.put(
        f"/students/{student_id}", json=updated_payload
    )
    assert updated.status_code == 200
    assert updated.json()["student"]["name"] == "Updated Student"

    deleted = authenticated_client.delete(f"/students/{student_id}")
    assert deleted.status_code == 200
    assert authenticated_client.get(f"/students/{student_id}").status_code == 404


def test_unauthenticated_student_request_is_rejected(client):
    response = client.get("/students/")

    assert response.status_code == 401


def test_user_cannot_access_another_users_student(client, authenticated_client):
    student = create_student(authenticated_client)
    second_credentials = {
        "username": f"other-user-{uuid.uuid4().hex}",
        "password": f"test-password-{uuid.uuid4().hex}",
    }
    assert client.post("/auth/register", json=second_credentials).status_code == 200
    login = client.post("/auth/login", json=second_credentials)
    client.headers.update(
        {"Authorization": f"Bearer {login.json()['access_token']}"}
    )

    response = client.get(f"/students/{student['id']}")

    assert response.status_code == 404


def test_name_and_course_filters_are_case_insensitive(authenticated_client):
    target = create_student(
        authenticated_client,
        name="Ava Example",
        course="Biology",
    )
    create_student(authenticated_client, name="No Match", course="History")

    response = authenticated_client.get(
        "/students/", params={"name": "AVA", "course": "bio"}
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [target["id"]]


def test_pagination_limits_and_skips_matching_students(authenticated_client):
    students = [
        create_student(authenticated_client, name=f"Page {number}")
        for number in range(3)
    ]

    response = authenticated_client.get(
        "/students/", params={"skip": 1, "limit": 1, "sort_by": "id"}
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [
        sorted(student["id"] for student in students)[1]
    ]


def test_sorting_orders_students_by_name(authenticated_client):
    create_student(authenticated_client, name="Zelda Example")
    create_student(authenticated_client, name="Amy Example")

    response = authenticated_client.get(
        "/students/", params={"sort_by": "name", "order": "desc"}
    )

    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == sorted(names, reverse=True)


@pytest.mark.parametrize(
    "overrides",
    [
        {"id": 0},
        {"name": "   "},
        {"name": "x" * 101},
        {"age": 0},
        {"course": "   "},
        {"course": "x" * 101},
    ],
)
def test_invalid_student_input_returns_validation_error(
    authenticated_client, overrides
):
    response = authenticated_client.post(
        "/students/", json=student_payload(**overrides)
    )

    assert response.status_code == 422
