import platform
import socket
from pathlib import Path
from datetime import timedelta


def get_uptime():
    """Return system uptime as a human-readable string."""
    uptime_seconds = float(Path("/proc/uptime").read_text().split()[0])
    return str(timedelta(seconds=int(uptime_seconds)))


def get_virtualization():
    """Detect whether the system is running inside a virtual machine."""
    try:
        result = Path("/sys/class/dmi/id/product_name").read_text().strip()
    except (FileNotFoundError, PermissionError):
        result = "Unknown"

    virtual_platforms = {
        "VMware Virtual Platform": "VMware",
        "VirtualBox": "VirtualBox",
        "KVM": "KVM",
        "QEMU": "QEMU",
        "Microsoft Corporation": "Hyper-V",
    }

    for product_name, platform_name in virtual_platforms.items():
        if product_name.lower() in result.lower():
            return {
                "is_virtual_machine": True,
                "virtualization": platform_name,
            }

    return {
        "is_virtual_machine": False,
        "virtualization": None,
    }


def collect_system_info():
    """Collect general system information."""
    virtualization = get_virtualization()

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "uptime": get_uptime(),
        **virtualization,
    }