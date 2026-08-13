import os
import psutil


def get_cpu_model():
    try:
        with open(
            "/proc/cpuinfo",
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()

                # ARM systems
                if line.startswith("Hardware"):
                    return line.split(":", 1)[1].strip()

    except OSError:
        pass

    return "Unknown"


def collect_cpu_info():

    try:
        load_1, load_5, load_15 = os.getloadavg()

    except OSError:
        load_1 = load_5 = load_15 = None

    freq = psutil.cpu_freq()

    per_core_utilization = psutil.cpu_percent(
        interval=1,
        percpu=True,
    )

    utilization_percent = round(
        sum(per_core_utilization) / len(per_core_utilization),
        1,
    ) if per_core_utilization else 0.0

    return {
        "model": get_cpu_model(),

        "physical_cores": psutil.cpu_count(
            logical=False
        ),

        "logical_cores": psutil.cpu_count(
            logical=True
        ),

        "frequency": {
            "current_mhz": (
                round(freq.current, 2)
                if freq
                else None
            ),
            "min_mhz": (
                round(freq.min, 2)
                if freq and freq.min > 0
                else None
            ),
            "max_mhz": (
                round(freq.max, 2)
                if freq and freq.max > 0
                else None
            ),
        },

        "utilization_percent": utilization_percent,

        "per_core_utilization": per_core_utilization,

        "load_average": {
            "1min": (
                round(load_1, 2)
                if load_1 is not None
                else None
            ),
            "5min": (
                round(load_5, 2)
                if load_5 is not None
                else None
            ),
            "15min": (
                round(load_15, 2)
                if load_15 is not None
                else None
            ),
        },
    }
