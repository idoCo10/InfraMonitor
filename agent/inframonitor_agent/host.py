import os
from pathlib import Path

HOST_ROOT = Path(
    os.getenv("INFRAMONITOR_HOST_ROOT", "/")
)


def host_path(path):
    """
    Return a path relative to the monitored host root.

    Native mode:
        /etc/os-release -> /etc/os-release

    Container host mode:
        /etc/os-release -> /host/etc/os-release
    """

    return HOST_ROOT / path.lstrip("/")


def is_host_mode():
    return HOST_ROOT != Path("/")