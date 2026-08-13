import platform
import socket
import subprocess
from pathlib import Path
from datetime import timedelta


def get_uptime():
    """Return system uptime as a human-readable string."""
    uptime_seconds = float(Path("/proc/uptime").read_text().split()[0])
    return str(timedelta(seconds=int(uptime_seconds)))


def get_os_name():
    """Return the human-readable OS name and version."""
    try:
        os_release = {}

        for line in Path("/etc/os-release").read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                os_release[key] = value.strip('"')

        return os_release.get("PRETTY_NAME", platform.system())

    except (FileNotFoundError, PermissionError):
        return platform.system()


def get_virtualization():
    """Detect virtualization platform and VMware Tools version."""
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

    for platform_product, platform_name in virtual_platforms.items():
        if platform_product.lower() in product_name.lower():
            virtualization = platform_name
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

                tools_version = result.stdout.strip()

                if tools_version:
                    virtualization = (
                        f"VMware (Tools version: "
                        f"{tools_version.replace('(build-', '[build-').replace(')', ']')})"
                    )
                    break

            except (
                subprocess.CalledProcessError,
                FileNotFoundError,
                subprocess.TimeoutExpired,
            ):
                pass

    return virtualization or "None"


def collect_system_info():
    """Collect general system information."""
    return {
        "hostname": socket.gethostname(),
        "os": get_os_name(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "uptime": get_uptime(),
        "virtualization": get_virtualization(),
    }