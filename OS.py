import platform
import os
import shutil
import json


def get_os_info():
    system = platform.system()

    if system == "Windows":
        os_name = "Windows"
        os_version = platform.win32_ver()[0]

    elif system == "Darwin":
        os_name = "macOS"
        os_version = platform.mac_ver()[0]

    elif system == "Linux":
        os_name = "Linux"

        try:
            linux_info = platform.freedesktop_os_release()
            os_version = linux_info.get(
                "PRETTY_NAME",
                platform.release()
            )
        except OSError:
            os_version = platform.release()

    else:
        os_name = "Unknown"
        os_version = "Unknown"

    return {
        "name": os_name,
        "version": os_version
    }


def get_disk_info():
    root_path = os.path.abspath(os.sep)

    disk = shutil.disk_usage(root_path)

    gib = 1024 ** 3

    return {
        "path": root_path,
        "total_gib": round(disk.total / gib, 2),
        "used_gib": round(disk.used / gib, 2),
        "free_gib": round(disk.free / gib, 2)
    }


def collect_system_info():
    return {
        "os": get_os_info(),

        "kernel": {
            "name": platform.system(),
            "release": platform.release(),
            "version": platform.version()
        },

        "hardware": {
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "logical_cpu_count": os.cpu_count(),
            "hostname": platform.node()
        },

        "python": {
            "version": platform.python_version()
        },

        "disk": get_disk_info()
    }


def save_to_json(data):
    with open("system_info.json", "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def main():
    data = collect_system_info()

    save_to_json(data)

    print(json.dumps(
        data,
        ensure_ascii=False,
        indent=4
    ))

    print("\nResult saved to system_info.json")


if __name__ == "__main__":
    main()