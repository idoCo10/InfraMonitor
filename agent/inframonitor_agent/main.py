from inframonitor_agent.collectors.system import collect_system_info


def main():
    system_info = collect_system_info()

    print("=== System Information ===")

    for key, value in system_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()