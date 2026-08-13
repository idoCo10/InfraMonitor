import socket

import psutil


def get_interface_addresses(interface):
    ipv4 = []
    ipv6 = []
    mac = None

    for address in interface:
        if address.family == psutil.AF_LINK:
            mac = address.address

        elif address.family == socket.AF_INET:
            ipv4.append(
                f"{address.address}/{address.netmask}"
                if address.netmask
                else address.address
            )

        elif address.family == socket.AF_INET6:
            ipv6.append(address.address.split("%")[0])

    return {
        "ipv4": ipv4,
        "ipv6": ipv6,
        "mac": mac,
    }


def get_interface_usage(interface_name):
    counters = psutil.net_io_counters(
        pernic=True
    )

    counter = counters.get(interface_name)

    if not counter:
        return {
            "total_bytes": 0,
            "rx_bytes": 0,
            "tx_bytes": 0,
        }

    return {
        "total_bytes": counter.bytes_recv + counter.bytes_sent,
        "rx_bytes": counter.bytes_recv,
        "tx_bytes": counter.bytes_sent,
    }


def collect_network_info():
    interface_addresses = psutil.net_if_addrs()
    interface_stats = psutil.net_if_stats()

    interfaces = []

    for interface_name, addresses in interface_addresses.items():

        stats = interface_stats.get(interface_name)

        if stats:
            is_up = stats.isup
            speed_mbps = stats.speed
            mtu = stats.mtu
        else:
            is_up = False
            speed_mbps = 0
            mtu = 0

        interface_info = {
            "name": interface_name,
            "is_up": is_up,
            "speed_mbps": speed_mbps,
            "mtu": mtu,
            "addresses": get_interface_addresses(addresses),
            "usage": get_interface_usage(interface_name),
        }

        interfaces.append(interface_info)

    # Show physical/real interfaces first and loopback last.
    interfaces.sort(
        key=lambda interface: interface["name"] == "lo"
    )

    return {
        "interfaces": interfaces,
        "total_interfaces": len(interfaces),
    }