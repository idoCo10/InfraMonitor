from fastapi.testclient import TestClient
from inframonitor_api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
    }


def test_receive_report():
    report = {
        "system": {
            "hostname": "test-server",
            "os": "Ubuntu",
        },
        "cpu": {
            "utilization_percent": 10.0,
        },
    }

    response = client.post(
        "/api/v1/reports",
        json=report,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "received"
    assert data["hostname"] == "test-server"
    assert isinstance(data["host_id"], int)
    assert isinstance(data["report_id"], int)


def test_get_host():
    report = {
        "system": {
            "hostname": "test-server",
            "os": "Ubuntu",
        },
        "cpu": {
            "utilization_percent": 10.0,
        },
    }

    client.post(
        "/api/v1/reports",
        json=report,
    )

    response = client.get(
        "/api/v1/hosts/test-server"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["hostname"] == "test-server"
    assert data["latest_report"]["system"]["os"] == "Ubuntu"
    assert data["latest_report"]["cpu"]["utilization_percent"] == 10.0


def test_get_host_not_found():
    response = client.get(
        "/api/v1/hosts/not-a-real-host"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Host not found"
    }