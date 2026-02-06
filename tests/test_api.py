from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_list_applications():
    payload = {
        "company": "TestCo",
        "role": "IT Support",
        "status": "applied",
        "notes": "test",
    }

    r = client.post("/applications", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["company"] == "TestCo"

    r2 = client.get("/applications")
    assert r2.status_code == 200
    items = r2.json()
    assert any(x["id"] == created["id"] for x in items)
