from inframonitor_agent.collectors.network import collect_network_info


def test_network_info():
    network_info = collect_network_info()

    assert network_info is not None
    assert "interfaces" in network_info
    assert "total_interfaces" in network_info

    assert isinstance(network_info["interfaces"], list)
    assert network_info["total_interfaces"] == len(
        network_info["interfaces"]
    )

    for interface in network_info["interfaces"]:
        assert "name" in interface
        assert "is_up" in interface
        assert "speed_mbps" in interface
        assert "mtu" in interface
        assert "addresses" in interface
        assert "usage" in interface

        assert isinstance(interface["is_up"], bool)
        assert interface["speed_mbps"] >= 0
        assert interface["mtu"] >= 0

        addresses = interface["addresses"]

        assert "ipv4" in addresses
        assert "ipv6" in addresses
        assert "mac" in addresses

        assert isinstance(addresses["ipv4"], list)
        assert isinstance(addresses["ipv6"], list)

        usage = interface["usage"]

        assert "total_bytes" in usage
        assert "rx_bytes" in usage
        assert "tx_bytes" in usage

        assert usage["total_bytes"] >= 0
        assert usage["rx_bytes"] >= 0
        assert usage["tx_bytes"] >= 0

        assert (
            usage["total_bytes"]
            == usage["rx_bytes"] + usage["tx_bytes"]
        )