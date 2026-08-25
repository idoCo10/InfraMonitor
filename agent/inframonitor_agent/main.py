import argparse
import json
import os
import time

from inframonitor_agent.client import send_report
from inframonitor_agent.collectors.cpu import collect_cpu_info
from inframonitor_agent.collectors.disk import collect_disk_info
from inframonitor_agent.collectors.memory import (
    collect_memory_info,
    get_memory_hardware,
)
from inframonitor_agent.collectors.network import collect_network_info
from inframonitor_agent.collectors.system import collect_system_info
from inframonitor_agent.display import print_report


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

    parser.add_argument(
        "--send",
        metavar="BACKEND_URL",
        default=os.getenv("INFRAMONITOR_BACKEND_URL"),
        help="Send collected system information to the InfraMonitor backend",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.getenv("INFRAMONITOR_INTERVAL", "0")),
        help="Send monitoring reports repeatedly at this interval in seconds",
    )

    args = parser.parse_args()

    if args.json:
        data = collect_all_info()
        print(json.dumps(data, indent=2))
        return

    if args.send:
        if args.interval:
            while True:
                data = collect_all_info()

                result = send_report(
                    data,
                    args.send,
                )

                print(
                    f"Report sent successfully "
                    f"for host: {result.get('hostname')}",
                    flush=True,
                )

                time.sleep(args.interval)

        else:
            data = collect_all_info()

            result = send_report(
                data,
                args.send,
            )

            print(
                f"Report sent successfully "
                f"for host: {result.get('hostname')}",
                flush=True,
            )

        return

    data = collect_all_info()
    print_report(data)


if __name__ == "__main__":
    main()