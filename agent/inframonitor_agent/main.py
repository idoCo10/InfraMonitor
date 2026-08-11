from inframonitor_agent.collectors.system import collect_system_info
from inframonitor_agent.collectors.cpu import collect_cpu_info


def main():
    
    system_info = collect_system_info()
    print("=== System Information ===")
    for key, value in system_info.items():
        print(f"{key}: {value}")


    cpu_info = collect_cpu_info()
    print("\n=== CPU Information ===")
    for key, value in cpu_info.items():
        print(f"{key}: {value}")        


if __name__ == "__main__":
    main()