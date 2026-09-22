import os
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

os.environ["DATABASE_URL"] = f"sqlite:///{Path(gettempdir()) / f'notes-test-{uuid4()}.db'}"

from fastapi.testclient import TestClient

from app.main import app


def test_notes_crud_and_pagination():
    with TestClient(app) as client:
        user_response = client.post(
            "/users",
            json={"email": "test@example.com", "phone": "+10000000000"},
        )
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        note_response = client.post(
            "/notes",
            json={"title": "Первая заметка", "user_id": user_id},
        )
        assert note_response.status_code == 201
        note = note_response.json()
        assert note["title"] == "Первая заметка"
        assert note["user_id"] == user_id

        list_response = client.get("/notes?skip=0&limit=1")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == 1
        assert len(list_response.json()["items"]) == 1

        update_response = client.patch(
            f"/notes/{note['id']}",
            json={"status": True},
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] is True

        delete_response = client.delete(f"/notes/{note['id']}")
        assert delete_response.status_code == 204
        assert client.get("/notes").json()["total"] == 0


def test_note_requires_existing_user():
    with TestClient(app) as client:
        response = client.post(
            "/notes",
            json={"title": "Без пользователя", "user_id": "missing"},
        )

    assert response.status_code == 404
    assert response.json()["code"] == "USER_NOT_FOUND"


def test_cors_header_is_present():
    with TestClient(app) as client:
        response = client.get("/", headers={"Origin": "http://localhost:3000"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
