import platform
import socket
import subprocess
from datetime import timedelta
from pathlib import Path


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
    virtualization = None
    vmware_tools_version = None

    # Primary detection method
    try:
        result = subprocess.run(
            ["systemd-detect-virt"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        detected = result.stdout.strip().lower()

        virtualization_names = {
            "kvm": "KVM",
            "qemu": "QEMU",
            "vmware": "VMware",
            "oracle": "VirtualBox",
            "microsoft": "Hyper-V",
            "xen": "Xen",
            "amazon": "Amazon EC2",
            "google": "Google Compute Engine",
        }

        if result.returncode == 0 and detected != "none":
            virtualization = virtualization_names.get(
                detected,
                detected.upper(),
            )

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        pass

    # Fallback to DMI if systemd-detect-virt
    # is unavailable or detects nothing.
    if virtualization is None:
        try:
            product_name = (
                Path("/sys/class/dmi/id/product_name")
                .read_text()
                .strip()
            )

            sys_vendor = (
                Path("/sys/class/dmi/id/sys_vendor")
                .read_text()
                .strip()
            )

            dmi_info = f"{sys_vendor} {product_name}".lower()

            virtual_platforms = {
                "vmware": "VMware",
                "virtualbox": "VirtualBox",
                "qemu": "QEMU",
                "kvm": "KVM",
                "microsoft": "Hyper-V",
                "linode": "KVM",
            }

            for identifier, platform_name in virtual_platforms.items():
                if identifier in dmi_info:
                    virtualization = platform_name
                    break

        except (FileNotFoundError, PermissionError, OSError):
            pass

    # VMware Tools version
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

    if virtualization == "VMware" and vmware_tools_version:
        version = vmware_tools_version.replace(
            " (build-",
            " [build-",
        ).replace(
            ")",
            "]",
        )

        virtualization_display = (
            f"VMware (Tools version: {version})"
        )

    else:
        virtualization_display = virtualization or "None"

    return virtualization_display


    

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