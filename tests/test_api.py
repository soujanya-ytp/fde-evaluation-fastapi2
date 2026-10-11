from fastapi.testclient import TestClient
from app.main import app, _tasks

client = TestClient(app)


def setup_function():
    _tasks.clear()


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_task_crud():
    created = client.post("/api/tasks", json={"title": "  Ship release ", "description": "v1"})
    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Ship release"
    task_id = task["id"]
    assert client.get(f"/api/tasks/{task_id}").status_code == 200
    updated = client.patch(f"/api/tasks/{task_id}", json={"completed": True})
    assert updated.json()["completed"] is True
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_blank_title_rejected():
    assert client.post("/api/tasks", json={"title": "   "}).status_code == 422
