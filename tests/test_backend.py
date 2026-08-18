from fastapi.testclient import TestClient
from inframonitor_api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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
    assert response.json() == {
        "status": "received",
        "hostname": "test-server",
    }
