from inframonitor_agent.collectors.cpu import collect_cpu_info


def test_cpu_info():
    cpu = collect_cpu_info()

    assert cpu["model"]
    assert cpu["physical_cores"] > 0
    assert cpu["logical_cores"] > 0

    assert "frequency" in cpu
    assert cpu["frequency"]["current_mhz"] is not None

    assert 0 <= cpu["utilization_percent"] <= 100

    assert len(cpu["per_core_utilization"]) == cpu["logical_cores"]

    assert "load_average" in cpu
    assert cpu["load_average"]["1min"] >= 0
    assert cpu["load_average"]["5min"] >= 0
    assert cpu["load_average"]["15min"] >= 0