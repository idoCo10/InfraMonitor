from inframonitor_agent.collectors.system import collect_system_info
from inframonitor_agent.collectors.cpu import collect_cpu_info
from inframonitor_agent.collectors.memory import (
    collect_memory_info,
    get_memory_hardware,
)


def main():

    system_info = collect_system_info()
    print("=== System Information ===")

    for key, value in system_info.items():
        print(f"{key}: {value}")

    cpu_info = collect_cpu_info()
    print("\n=== CPU Information ===")

    for key, value in cpu_info.items():
        print(f"{key}: {value}")

    memory_hardware = get_memory_hardware()

    if memory_hardware:
        print("\n=== Memory Hardware ===")
        print(f"Source:             {memory_hardware['source']}")
        print(f"Reliability:        {memory_hardware['reliability']}")
        print(f"Reported Modules:   {memory_hardware['installed_modules']}")
        print(f"Maximum Capacity:   {memory_hardware['maximum_capacity']}")

        for module in memory_hardware["modules"]:
            print(f"\n{module['locator']}: {module['size']}")
            print(f"  Type:           {module['type']}")
            print(f"  Speed:          {module['speed']}")
            print(f"  Configured:     {module['configured_speed']}")
            print(f"  Manufacturer:   {module['manufacturer']}")
            print(f"  Part Number:    {module['part_number']}")

    memory_info = collect_memory_info()

    print("\n=== Memory Information ===")

    ram = memory_info["ram"]

    print(f"Total:        {ram['total_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Used:         {ram['used_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Available:    {ram['available_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Utilization:  {ram['utilization_percent']:.1f}%")

    print("\n=== Swap Information ===")

    swap = memory_info["swap"]

    print(f"Total:        {swap['total_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Used:         {swap['used_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Free:         {swap['free_bytes'] / (1024 ** 3):.2f} GB")
    print(f"Utilization:  {swap['utilization_percent']:.1f}%")


if __name__ == "__main__":
    main()