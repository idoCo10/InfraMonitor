import os
import psutil


def get_cpu_model():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass

    return "Unknown"


def collect_cpu_info():
    load_1, load_5, load_15 = os.getloadavg()

    freq = psutil.cpu_freq()

    return {
        "model": get_cpu_model(),

        "physical_cores": psutil.cpu_count(logical=False),

        "logical_cores": psutil.cpu_count(logical=True),

        "frequency": {
            "current_mhz": round(freq.current, 2) if freq else None,
            "min_mhz": round(freq.min, 2) if freq and freq.min > 0 else None,
            "max_mhz": round(freq.max, 2) if freq and freq.max > 0 else None,
        },

        "utilization_percent": psutil.cpu_percent(interval=1),

        "per_core_utilization": psutil.cpu_percent(
            interval=1,
            percpu=True,
        ),

        "load_average": {
            "1min": round(load_1, 2),
            "5min": round(load_5, 2),
            "15min": round(load_15, 2),
        },
    }