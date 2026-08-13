from inframonitor_agent.collectors.system import collect_system_info
from inframonitor_agent.collectors.cpu import collect_cpu_info
from inframonitor_agent.collectors.memory import (
    collect_memory_info,
    get_memory_hardware,
)
from inframonitor_agent.collectors.disk import collect_disk_info


def format_gb(bytes_value):
    return bytes_value / (1024 ** 3)


def print_usage(usage, indent="       "):
    if not usage:
        return

    print(f"{indent}Total:       {format_gb(usage['total_bytes']):.2f} GB")
    print(f"{indent}Used:        {format_gb(usage['used_bytes']):.2f} GB")
    print(f"{indent}Free:        {format_gb(usage['free_bytes']):.2f} GB")
    print(f"{indent}Utilization: {usage['utilization_percent']:.1f}%")


def main():

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

    for key, value in cpu_info.items():
        print(f"{key}: {value}")

    # =========================
    # Memory Hardware
    # =========================

    memory_info = collect_memory_info()

    print("\n=== Memory Information ===")

    ram = memory_info["ram"]
    swap = memory_info["swap"]

    print(f"Total:        {ram['total_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Used:         {ram['used_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Available:    {ram['available_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Utilization:  {ram['utilization_percent']:.1f}%")

    if swap["total_bytes"] == 0:
        print("Swap:         None")
    else:
        print(f"Swap Total:       {swap['total_bytes'] / (1024 ** 3):.2f} GB")
        print(f"Swap Used:        {swap['used_bytes'] / (1024 ** 3):.2f} GB")
        print(f"Swap Available:   {swap['free_bytes'] / (1024 ** 3):.2f} GB")
        print(f"Swap Utilization: {swap['utilization_percent']:.1f}%")

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
        print(f"  Bus:         {disk['bus'] or 'Unknown'}")
        print(f"  Media Type:  {disk['media_type']}")
        print(f"  Vendor:      {disk['vendor'] or 'Unknown'}")
        print(f"  Model:       {disk['model'] or 'Unknown'}")
        print(f"  Serial:      {disk['serial'] or 'Unknown'}")
        print(f"  Partitions:  {len(disk['partitions'])}")

        for index, partition in enumerate(
            disk["partitions"],
            start=1,
        ):
            print(f"\n  {index}. {partition['name']}")
            print(f"     Size:        {partition['size']}")
            print(f"     Type:        {partition['type']}")

            if partition["filesystem"]:
                print(f"     Filesystem:  {partition['filesystem']}")

            print(f"     Mountpoints: {partition['mountpoints']}")

            if partition.get("usage"):
                print_usage(
                    partition["usage"],
                    indent="     ",
                )

            for lv in partition["logical_volumes"]:

                print(f"\n     Logical Volume: {lv['name']}")
                print(f"       Size:        {lv['size']}")
                print(f"       Type:        {lv['type']}")

                if lv["filesystem"]:
                    print(f"       Filesystem:  {lv['filesystem']}")

                print(f"       Mountpoints: {lv['mountpoints']}")

                if lv.get("usage"):
                    print_usage(
                        lv["usage"],
                        indent="       ",
                    )


if __name__ == "__main__":
    main()