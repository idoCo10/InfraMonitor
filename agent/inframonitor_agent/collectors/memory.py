import psutil
import subprocess
import re


def collect_memory_info():
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()

    return {
        "ram": {
            "total_bytes": virtual_memory.total,
            "used_bytes": virtual_memory.used,
            "available_bytes": virtual_memory.available,
            "free_bytes": virtual_memory.free,
            "utilization_percent": virtual_memory.percent,
        },
        "swap": {
            "total_bytes": swap_memory.total,
            "used_bytes": swap_memory.used,
            "free_bytes": swap_memory.free,
            "utilization_percent": swap_memory.percent,
        },
    }


def get_memory_hardware():
    try:
        result = subprocess.run(
            ["sudo", "-n", "dmidecode", "--type", "memory"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode != 0:
            return None

        output = result.stdout

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

    modules = []

    # Extract only DMI type 17 (Memory Device) sections
    devices = re.findall(
        r"(Handle .*?DMI type 17.*?)(?=\nHandle |\Z)",
        output,
        re.DOTALL,
    )

    for device in devices:

        size_match = re.search(r"Size:\s+(.+)", device)

        if not size_match:
            continue

        size = size_match.group(1).strip()

        # Ignore empty RAM slots
        if size.lower() == "no module installed":
            continue

        def get_value(field):
            match = re.search(rf"{field}:\s+(.+)", device)
            return match.group(1).strip() if match else None

        modules.append({
            "size": size,
            "type": get_value("Type"),
            "speed": get_value("Speed"),
            "configured_speed": get_value("Configured Memory Speed"),
            "manufacturer": get_value("Manufacturer"),
            "part_number": get_value("Part Number"),
            "locator": get_value("Locator"),
        })

    # Maximum capacity
    max_capacity_match = re.search(
        r"Maximum Capacity:\s+(.+)",
        output,
    )

    max_capacity = (
        max_capacity_match.group(1).strip()
        if max_capacity_match
        else None
    )

    return {
        "modules": modules,
        "installed_modules": len(modules),
        "maximum_capacity": max_capacity,
    }