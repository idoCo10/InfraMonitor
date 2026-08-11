from inframonitor_agent.collectors.system import collect_system_info


def test_system_info():
    info = collect_system_info()

    assert info["hostname"]
    assert info["os"]
    assert info["os_version"]
    assert info["kernel"]
    assert info["architecture"]
    assert info["uptime"]
    assert isinstance(info["is_virtual_machine"], bool)