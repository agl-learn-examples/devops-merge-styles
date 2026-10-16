import pytest
import app as tasks_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)          # tasks.db is made in a fresh folder for each test
    return tasks_app.app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_create_and_list(client):
    r = client.post("/tasks", json={"title": "learn HTTP"})
    assert r.status_code == 201
    assert client.get("/tasks").get_json() == [{"id": 1, "title": "learn HTTP", "done": False}]


def test_filter_by_done(client):
    client.post("/tasks", json={"title": "a"})
    client.put("/tasks/1", json={"title": "a", "done": True})
    client.post("/tasks", json={"title": "b"})
    assert [t["title"] for t in client.get("/tasks?done=true").get_json()] == ["a"]
    assert [t["title"] for t in client.get("/tasks?done=false").get_json()] == ["b"]


def test_title_required(client):
    assert client.post("/tasks", json={}).status_code == 400
