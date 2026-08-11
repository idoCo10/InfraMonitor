import platform
import socket
import subprocess
from pathlib import Path
from datetime import timedelta


def get_uptime():
    """Return system uptime as a human-readable string."""
    uptime_seconds = float(Path("/proc/uptime").read_text().split()[0])
    return str(timedelta(seconds=int(uptime_seconds)))


def get_virtualization():
    try:
        product_name = (
            Path("/sys/class/dmi/id/product_name")
            .read_text()
            .strip()
        )
    except (FileNotFoundError, PermissionError):
        product_name = "Unknown"

    virtual_platforms = {
        "VMware Virtual Platform": "VMware",
        "VirtualBox": "VirtualBox",
        "KVM": "KVM",
        "QEMU": "QEMU",
        "Microsoft Corporation": "Hyper-V",
    }

    virtualization = None
    is_virtual_machine = False
    vmware_tools_version = None

    for platform_product, platform_name in virtual_platforms.items():
        if platform_product.lower() in product_name.lower():
            virtualization = platform_name
            is_virtual_machine = True
            break

    if virtualization == "VMware":
        commands = [
            ["vmware-toolbox-cmd", "-v"],
            ["vmtoolsd", "--version"],
        ]

        for cmd in commands:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=True,
                )

                vmware_tools_version = result.stdout.strip()
                break

            except (
                subprocess.CalledProcessError,
                FileNotFoundError,
                subprocess.TimeoutExpired,
            ):
                pass

    return {
        "is_virtual_machine": is_virtual_machine,
        "virtualization": virtualization,
        "vmware_tools_version": vmware_tools_version,
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