#from inframonitor_agent.collectors.cpu import (
    collect_cpu_info,
)


def test_cpu_info():
    cpu = collect_cpu_info()

    assert cpu["model"]

    assert isinstance(
        cpu["physical_cores"],
        int,
    )
    assert cpu["physical_cores"] > 0

    assert isinstance(
        cpu["logical_cores"],
        int,
    )
    assert (
        cpu["logical_cores"]
        >= cpu["physical_cores"]
    )

    assert isinstance(
        cpu["frequency"],
        dict,
    )

    assert (
        cpu["frequency"]["current_mhz"]
        is None
        or cpu["frequency"]["current_mhz"] > 0
    )

    assert (
        0
        <= cpu["utilization_percent"]
        <= 100
    )

    assert isinstance(
        cpu["per_core_utilization"],
        list,
    )

    assert (
        len(cpu["per_core_utilization"])
        == cpu["logical_cores"]
    )

    for core in cpu["per_core_utilization"]:
        assert 0 <= core <= 100

    assert isinstance(
        cpu["load_average"],
        dict,
    )