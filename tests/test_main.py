from unittest.mock import patch

from inframonitor_agent.main import collect_all_info, main


def test_collect_all_info():
    data = collect_all_info()

    assert "system" in data
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data
    assert "network" in data

    assert data["system"]["hostname"]
    assert data["cpu"]["logical_cores"] > 0
    assert data["memory"]["ram"]["total_bytes"] > 0

    assert "disks" in data["disk"]
    assert "interfaces" in data["network"]


def test_interval_send():
    test_args = [
        "inframonitor",
        "--send",
        "http://127.0.0.1:8000",
        "--interval",
        "10",
    ]

    with (
        patch("sys.argv", test_args),
        patch(
            "inframonitor_agent.main.collect_all_info",
            return_value={"system": {"hostname": "test-server"}},
        ),
        patch("inframonitor_agent.main.send_report") as mock_send,
        patch(
            "inframonitor_agent.main.time.sleep",
            side_effect=KeyboardInterrupt,
        ),
    ):
        try:
            main()
        except KeyboardInterrupt:
            pass

    mock_send.assert_called_once_with(
        {"system": {"hostname": "test-server"}},
        "http://127.0.0.1:8000",
    )    