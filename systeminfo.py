import platform
import sys

def get_system_info():
    info = {
        "Python Version": sys.version,
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
    }
    return info

def main():
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
