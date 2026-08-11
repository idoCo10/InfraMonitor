from inframonitor_agent.collectors.memory import (
    collect_memory_info,
    get_memory_hardware,
)


def test_memory_info():
    memory = collect_memory_info()

    assert "ram" in memory
    assert "swap" in memory

    ram = memory["ram"]
    swap = memory["swap"]

    assert ram["total_bytes"] > 0
    assert ram["used_bytes"] >= 0
    assert ram["available_bytes"] >= 0
    assert ram["free_bytes"] >= 0
    assert 0 <= ram["utilization_percent"] <= 100

    assert swap["total_bytes"] >= 0
    assert swap["used_bytes"] >= 0
    assert swap["free_bytes"] >= 0
    assert 0 <= swap["utilization_percent"] <= 100


def test_memory_hardware():
    memory = get_memory_hardware()

    # Hardware information may not be available
    # on every environment (e.g. some containers/cloud VMs).
    if memory is None:
        return

    assert "modules" in memory
    assert "installed_modules" in memory
    assert "maximum_capacity" in memory

    assert isinstance(memory["modules"], list)
    assert memory["installed_modules"] == len(memory["modules"])

    for module in memory["modules"]:
        assert "size" in module
        assert "type" in module
        assert "speed" in module
        assert "configured_speed" in module
        assert "manufacturer" in module
        assert "part_number" in module
        assert "locator" in module