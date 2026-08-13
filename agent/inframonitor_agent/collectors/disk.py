import json
import os
import subprocess

import psutil


def get_disk_usage(mountpoint):
    try:
        usage = psutil.disk_usage(mountpoint)

        return {
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "utilization_percent": usage.percent,
        }

    except (PermissionError, FileNotFoundError, OSError):
        return None


def get_mountpoints(device):
    mountpoints = []

    for partition in psutil.disk_partitions(all=True):
        if partition.device == device:
            mountpoints.append(partition.mountpoint)

    return mountpoints if mountpoints else [None]


def get_device_name(device):
    return os.path.basename(device)


def get_disk_bus(device_name):
    try:
        path = f"/sys/block/{device_name}/device/subsystem"

        if os.path.islink(path):
            return os.path.basename(os.readlink(path))

    except (FileNotFoundError, OSError):
        pass

    return None


def get_media_type(device_name, vendor=None, model=None):
    """
    Determine whether a disk is virtual, HDD, SSD, or unknown.

    Virtual disk detection takes priority over rotational detection.
    """

    device_info = f"{vendor or ''} {model or ''}".lower()

    virtual_identifiers = [
        "vmware",
        "qemu",
        "virtualbox",
        "virtual disk",
        "virtual hard disk",
        "microsoft virtual",
    ]

    for identifier in virtual_identifiers:
        if identifier in device_info:
            return "Virtual Disk"

    try:
        with open(
            f"/sys/block/{device_name}/queue/rotational",
            "r",
            encoding="utf-8",
        ) as file:
            rotational = file.read().strip()

        if rotational == "0":
            return "SSD"

        if rotational == "1":
            return "HDD"

    except (FileNotFoundError, PermissionError, OSError):
        pass

    return "Unknown"


def get_disk_hardware():
    try:
        result = subprocess.run(
            [
                "lsblk",
                "-J",
                "-o",
                "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,"
                "MODEL,VENDOR,SERIAL",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None

    try:
        data = json.loads(result.stdout)

    except (json.JSONDecodeError, TypeError):
        return None

    disks = []

    for disk in data.get("blockdevices", []):
        if disk.get("type") != "disk":
            continue

        disk_name = disk.get("name")

        if not disk_name:
            continue

        vendor = (disk.get("vendor") or "").strip(" ,")
        model = (disk.get("model") or "").strip()
        serial = (disk.get("serial") or "").strip()

        disk_info = {
            "name": disk_name,
            "size": disk.get("size"),
            "type": disk.get("type"),
            "bus": get_disk_bus(disk_name),
            "media_type": get_media_type(
                disk_name,
                vendor=vendor,
                model=model,
            ),
            "vendor": vendor or None,
            "model": model or None,
            "serial": serial or None,
            "partitions": [],
        }

        children = disk.get("children") or []

        for partition in children:
            partition_name = partition.get("name")

            if not partition_name:
                continue

            partition_info = {
                "name": partition_name,
                "size": partition.get("size"),
                "type": partition.get("type"),
                "filesystem": partition.get("fstype"),
                "mountpoints": partition.get("mountpoints")
                or [None],
                "logical_volumes": [],
            }

            # Check if this partition contains LVM logical volumes.
            logical_volumes = partition.get("children") or []

            for lv in logical_volumes:
                if lv.get("type") != "lvm":
                    continue

                lv_info = {
                    "name": lv.get("name"),
                    "size": lv.get("size"),
                    "type": lv.get("type"),
                    "filesystem": lv.get("fstype"),
                    "mountpoints": lv.get("mountpoints")
                    or [None],
                    "usage": None,
                }

                # Get usage for mounted logical volume.
                for mountpoint in lv_info["mountpoints"]:
                    if mountpoint:
                        usage = get_disk_usage(mountpoint)

                        if usage:
                            lv_info["usage"] = usage
                            break

                partition_info["logical_volumes"].append(lv_info)

            # Get usage for the partition itself.
            for mountpoint in partition_info["mountpoints"]:
                if mountpoint:
                    usage = get_disk_usage(mountpoint)

                    if usage:
                        partition_info["usage"] = usage
                        break
            else:
                partition_info["usage"] = None

            disk_info["partitions"].append(partition_info)

        disks.append(disk_info)

    return {
        "disks": disks,
        "total_disks": len(disks),
    }


def collect_disk_info():
    """
    Collect disk hardware information and filesystem usage.
    """

    return get_disk_hardware()