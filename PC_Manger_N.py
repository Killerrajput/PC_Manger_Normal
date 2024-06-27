import os
import platform

def get_system_info():
    system_info = {
        "Operating System": platform.system(),
        "System Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Total Memory": get_total_memory(),
        "Available Memory": get_available_memory(),
        "Disk Usage": get_disk_usage()
    }
    return system_info

def get_total_memory():
    if platform.system() == 'Windows':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        memory = ctypes.c_ulonglong(0)
        kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
        return f"{memory.value / (1024 ** 3):.2f} GB"
    else:
        with open('/proc/meminfo', 'r') as mem:
            for line in mem:
                if 'MemTotal' in line:
                    return f"{int(line.split()[1]) / 1024:.2f} GB"
    return "Unknown"

def get_available_memory():
    if platform.system() == 'Windows':
        import psutil
        return f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB"
    else:
        with open('/proc/meminfo', 'r') as mem:
            for line in mem:
                if 'MemAvailable' in line:
                    return f"{int(line.split()[1]) / 1024:.2f} GB"
    return "Unknown"

def get_disk_usage():
    if platform.system() == 'Windows':
        import psutil
        return f"{psutil.disk_usage('/').percent}%"
    else:
        import subprocess
        df = subprocess.Popen(["df", "-h", "/"], stdout=subprocess.PIPE)
        output = df.communicate()[0].decode("utf-8").strip().split("\n")[-1].split()
        return output[-2]

def optimize_system():
    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.winmm.SetProcessWorkingSetSize(-1, -1)
        return True
    else:
        return False

def main():
    system_info = get_system_info()
    print("System Information:")
    for key, value in system_info.items():
        print(f"{key}: {value}")

    print("\nOptimizing System...")
    if optimize_system():
        print("System optimization successful.")
    else:
        print("System optimization not supported on this platform.")

if __name__ == "__main__":
    main()
