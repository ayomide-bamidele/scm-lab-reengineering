import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from migrate import migrate


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDENTS_DB", str(tmp_path / "test.db"))
    return TestClient(app)


def test_empty_stats(client):
    assert client.get("/stats").json()["count"] == 0
    assert client.get("/students").json() == []


def test_create_list_get_delete(client):
    created = client.post("/students", json={"name": " Ada ", "score": 91})
    assert created.status_code == 201 and created.json()["name"] == "Ada"
    sid = created.json()["id"]
    assert client.get(f"/students/{sid}").json()["score"] == 91
    assert len(client.get("/students").json()) == 1
    assert client.delete(f"/students/{sid}").status_code == 204
    assert client.get(f"/students/{sid}").status_code == 404


@pytest.mark.parametrize("payload", [{"name": "", "score": 50}, {"name": "Bob", "score": 150}, {"name": "Bob", "score": -1}])
def test_validation_rejected(client, payload):
    assert client.post("/students", json=payload).status_code == 422


def test_migration_is_idempotent_and_stats(client, tmp_path):
    src = tmp_path / "s.json"
    src.write_text(json.dumps([{"name": "A", "score": 40}, {"name": "B", "score": 60}, {"name": "C", "score": 90}]))
    assert migrate(str(src)) == 3
    assert migrate(str(src)) == 0
    stats = client.get("/stats").json()
    assert stats == {"count": 3, "average": 63.33, "median": 60, "highest": 90, "lowest": 40}
