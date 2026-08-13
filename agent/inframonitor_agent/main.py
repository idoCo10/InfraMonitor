import argparse
import json

from inframonitor_agent.collectors.system import collect_system_info
from inframonitor_agent.collectors.cpu import collect_cpu_info
from inframonitor_agent.collectors.memory import (
    collect_memory_info,
    get_memory_hardware,
)
from inframonitor_agent.collectors.disk import collect_disk_info
from inframonitor_agent.collectors.network import collect_network_info




def format_gb(bytes_value):
    return bytes_value / (1024 ** 3)


def format_bytes(bytes_value):
    if bytes_value < 1024:
        return f"{bytes_value:.0f} B"

    if bytes_value < 1024 ** 2:
        return f"{bytes_value / 1024:.1f} KB"

    if bytes_value < 1024 ** 3:
        return f"{bytes_value / (1024 ** 2):.1f} MB"

    return f"{bytes_value / (1024 ** 3):.2f} GB"


def print_usage(usage, indent="       "):
    if not usage:
        return

    print(
        f"{indent}Total:       "
        f"{format_gb(usage['total_bytes']):.2f} GB"
    )
    print(
        f"{indent}Used:        "
        f"{format_gb(usage['used_bytes']):.2f} GB"
    )
    print(
        f"{indent}Free:        "
        f"{format_gb(usage['free_bytes']):.2f} GB"
    )
    print(
        f"{indent}Utilization: "
        f"{usage['utilization_percent']:.1f}%"
    )


def format_mountpoints(mountpoints):
    valid_mountpoints = [
        mountpoint
        for mountpoint in mountpoints
        if mountpoint
    ]

    if not valid_mountpoints:
        return "None"

    cleaned_mountpoints = [
        "SWAP" if mountpoint == "[SWAP]" else mountpoint
        for mountpoint in valid_mountpoints
    ]

    return ", ".join(cleaned_mountpoints)


def collect_all_info():
    system_info = collect_system_info()

    data = {
        "system": system_info,
        "cpu": collect_cpu_info(),
        "memory": collect_memory_info(),
        "disk": collect_disk_info(),
        "network": collect_network_info(),
    }

    if system_info["virtualization"] == "None":
        memory_hardware = get_memory_hardware()

        if memory_hardware:
            data["memory_hardware"] = memory_hardware

    return data




def main():

    parser = argparse.ArgumentParser(
        description="InfraMonitor system information collector"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output system information as JSON",
    )

    args = parser.parse_args()

    if args.json:
        data = collect_all_info()
        print(json.dumps(data, indent=2))
        return

    # =========================
    # System
    # =========================

    system_info = collect_system_info()

    print("=== System Information ===")
    print(f"Hostname:                 {system_info['hostname']}")
    print(f"OS:                       {system_info['os']}")
    print(f"Kernel:                   {system_info['kernel']}")
    print(f"Architecture:             {system_info['architecture']}")
    print(f"Uptime:                   {system_info['uptime']}")
    print(f"Virtualization:           {system_info['virtualization']}")


    # =========================
    # CPU
    # =========================

    cpu_info = collect_cpu_info()

    print("\n=== CPU Information ===")

    print(
        f"Model:                 "
        f"{cpu_info['model']}"
    )

    if system_info["virtualization"]:
        print(
            f"vCPUs:                 "
            f"{cpu_info['logical_cores']}"
        )
    else:
        print(
            f"Physical Cores:        "
            f"{cpu_info['physical_cores']}"
        )
        print(
            f"Logical Cores:         "
            f"{cpu_info['logical_cores']}"
        )

    frequency = cpu_info["frequency"]

    if frequency["current_mhz"] is not None:
        print(
            f"Frequency:             "
            f"{frequency['current_mhz']:.2f} MHz"
        )
    else:
        print("Frequency:             Unknown")

    print(
        f"CPU Utilization:       "
        f"{cpu_info['utilization_percent']:.1f}%"
    )

    per_core = ", ".join(
        f"{value:.1f}%"
        for value in cpu_info["per_core_utilization"]
    )

    print("Per-Core Utilization:")

    for core_index, utilization in enumerate(
        cpu_info["per_core_utilization"]
    ):
        print(
            f"  Core {core_index}: "
            f"{utilization:.1f}%"
        )

    load = cpu_info["load_average"]

    print(
        f"Load Average:          "
        f"1m: {load['1min']:.2f}, "
        f"5m: {load['5min']:.2f}, "
        f"15m: {load['15min']:.2f}"
    )

    # =========================
    # Memory
    # =========================

    memory_info = collect_memory_info()

    print("\n=== Memory Information ===")

    ram = memory_info["ram"]
    swap = memory_info["swap"]

    print(
        f"{'Total:':<18}"
        f"{format_gb(ram['total_bytes']):.2f} GB"
    )
    print(
        f"{'Used:':<18}"
        f"{format_gb(ram['used_bytes']):.2f} GB"
    )
    print(
        f"{'Available:':<18}"
        f"{format_gb(ram['available_bytes']):.2f} GB"
    )
    print(
        f"{'Utilization:':<18}"
        f"{ram['utilization_percent']:.1f}%"
    )

    if swap["total_bytes"] == 0:
        print(f"{'Swap:':<18}None")
    else:
        print(
            f"{'Swap Total:':<18}"
            f"{format_gb(swap['total_bytes']):.2f} GB"
        )
        print(
            f"{'Swap Used:':<18}"
            f"{format_gb(swap['used_bytes']):.2f} GB"
        )
        print(
            f"{'Swap Available:':<18}"
            f"{format_gb(swap['free_bytes']):.2f} GB"
        )
        print(
            f"{'Swap Utilization:':<18}"
            f"{swap['utilization_percent']:.1f}%"
        )


    # =========================
    # Memory Hardware
    # =========================

    is_virtual_machine = system_info["virtualization"] != "None"

    if not is_virtual_machine:
        memory_hardware = get_memory_hardware()

        if memory_hardware:
            print("\n=== Memory Hardware ===")

            print(
                f"Installed Modules: "
                f"{memory_hardware['installed_modules']}"
            )

            print(
                f"Maximum Capacity:  "
                f"{memory_hardware['maximum_capacity'] or 'Unknown'}"
            )

            for index, module in enumerate(
                memory_hardware["modules"],
                start=1,
            ):
                print(f"\nDIMM {index}")
                print(
                    f"  Size:          "
                    f"{module['size'] or 'Unknown'}"
                )
                print(
                    f"  Type:          "
                    f"{module['type'] or 'Unknown'}"
                )
                print(
                    f"  Speed:         "
                    f"{module['speed'] or 'Unknown'}"
                )
                print(
                    f"  Config Speed:  "
                    f"{module['configured_speed'] or 'Unknown'}"
                )
                print(
                    f"  Manufacturer:  "
                    f"{module['manufacturer'] or 'Unknown'}"
                )
                print(
                    f"  Part Number:   "
                    f"{module['part_number'] or 'Unknown'}"
                )
                print(
                    f"  Slot:          "
                    f"{module['locator'] or 'Unknown'}"
                )


    # =========================
    # Disk
    # =========================

    disk_info = collect_disk_info()

    print("\n=== Disk Information ===")

    if not disk_info:
        print("Disk information unavailable.")
        return

    print(f"Total Disks: {disk_info['total_disks']}")

    for disk in disk_info["disks"]:

        print(f"\nDisk: {disk['name']}")
        print(f"  Size:        {disk['size']}")
        print(f"  Type:        {disk['type']}")
        if disk.get("bus"):
            print(f"  Bus:         {disk['bus']}")

        if disk.get("media_type") and disk["media_type"] != "Unknown":
            print(f"  Media Type:  {disk['media_type']}")

        if disk.get("vendor"):
            print(f"  Vendor:      {disk['vendor']}")

        if disk.get("model"):
            print(f"  Model:       {disk['model']}")

        if disk.get("serial"):
            print(f"  Serial:      {disk['serial']}")

        if disk.get("filesystem"):
            print(f"  Filesystem:  {disk['filesystem']}")

        disk_mountpoints = [
            mountpoint
            for mountpoint in disk.get("mountpoints", [])
            if mountpoint
        ]

        if disk_mountpoints:
            label = "Mountpoint:" if len(disk_mountpoints) == 1 else "Mountpoints:"

            print(
                f"  {label:<13}"
                f"{format_mountpoints(disk_mountpoints)}"
            )

        if disk.get("usage"):
            print_usage(
                disk["usage"],
                indent="  ",
            )

        print(f"  Partitions:  {len(disk['partitions'])}")

        for index, partition in enumerate(
            disk["partitions"],
            start=1,
        ):
            print(f"\n  {index}. {partition['name']}")
            print(f"     Size:        {partition['size']}")
            print(f"     Type:        {partition['type']}")

            if partition["filesystem"]:
                print(
                    f"     Filesystem:  "
                    f"{partition['filesystem']}"
                )

            print(
                f"     Mountpoints: "
                f"{format_mountpoints(partition['mountpoints'])}"
            )

            if partition.get("usage"):
                print_usage(
                    partition["usage"],
                    indent="     ",
                )

            for lv in partition["logical_volumes"]:

                print(
                    f"\n     Logical Volume: "
                    f"{lv['name']}"
                )
                print(f"       Size:        {lv['size']}")
                print(f"       Type:        {lv['type']}")

                if lv["filesystem"]:
                    print(
                        f"       Filesystem:  "
                        f"{lv['filesystem']}"
                    )

                print(
                    f"       Mountpoints: "
                    f"{format_mountpoints(lv['mountpoints'])}"
                )

                if lv.get("usage"):
                    print_usage(
                        lv["usage"],
                        indent="       ",
                    )

    # =========================
    # Network
    # =========================

    network_info = collect_network_info()

    print("\n=== Network Information ===")

    if not network_info:
        print("Network information unavailable.")
        return

    for interface in network_info["interfaces"]:

        print(f"\nInterface: {interface['name']}")
        print(
            f"  Status:       "
            f"{'UP' if interface['is_up'] else 'DOWN'}"
        )
        speed = interface["speed_mbps"]

        if speed and speed > 0:
            print(f"  Speed:        {speed} Mbps")
        else:
            print("  Speed:        N/A")
        print(
            f"  MTU:          "
            f"{interface['mtu']}"
        )

        addresses = interface["addresses"]

        print(
            f"  MAC:          "
            f"{addresses['mac'] or 'Unknown'}"
        )

        if addresses["ipv4"]:
            print(
                f"  IPv4:         "
                f"{', '.join(addresses['ipv4'])}"
            )

        if addresses["ipv6"]:
            print(
                f"  IPv6:         "
                f"{', '.join(addresses['ipv6'])}"
            )

        usage = interface["usage"]

        print(
            f"  Usage:        "
            f"Total: {format_bytes(usage['total_bytes'])} "
            f"(RX: {format_bytes(usage['rx_bytes'])}, "
            f"TX: {format_bytes(usage['tx_bytes'])})"
        )


if __name__ == "__main__":
    main()