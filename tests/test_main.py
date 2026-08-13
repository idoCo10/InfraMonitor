from inframonitor_agent.main import collect_all_info


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