#!/usr/bin/env python3
import os
import platform
import re
import shutil
import subprocess
import time


def run_command(command):
    try:
        return subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""


def detect_windows_cpu():
    output = run_command("wmic cpu get Name /value")
    match = re.search(r"Name=(.+)", output)
    cpu_name = match.group(1).strip() if match else ""
    
    if not cpu_name:
        cpu_name = platform.processor().strip()
    
    return cpu_name if cpu_name else "Unknown"


def detect_windows_gpu():
    output = run_command("wmic path win32_VideoController get Name /value")
    match = re.search(r"Name=(.+)", output)
    return match.group(1).strip() if match else "Unknown"


def detect_windows_ram():
    output = run_command("wmic computersystem get TotalPhysicalMemory /value")
    match = re.search(r"TotalPhysicalMemory=(\d+)", output)
    if match:
        return str(round(int(match.group(1)) / 1024 / 1024))
    return "Unknown"


def detect_windows_storage():
    drives = []
    try:
        output = run_command("wmic diskdrive get Model,Size")
        lines = output.strip().split("\n")[1:]
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                size_bytes = parts[-1]
                model = " ".join(parts[:-1])
                if size_bytes.isdigit() and model:
                    size_gib = round(int(size_bytes) / 1024 / 1024 / 1024)
                    drives.append(f"{model} ({size_gib} GiB)")
        
        if drives:
            return "\n".join(drives)
    except Exception:
        pass
    
    return "Unknown"


def detect_posix_cpu():
    cpu_name = ""
    freq_mhz = ""
    if os.path.exists("/proc/cpuinfo"):
        output = run_command("cat /proc/cpuinfo")
        match = re.search(r"model name\s*:\s*(.+)", output)
        if match:
            cpu_name = match.group(1).strip()
        freq_match = re.search(r"cpu MHz\s*:\s*([0-9.]+)", output)
        if freq_match:
            freq_mhz = f" @ {float(freq_match.group(1)) / 1000:.2f}GHz"
    if platform.system() == "Darwin":
        output = run_command("sysctl -n machdep.cpu.brand_string")
        if output:
            cpu_name = output.strip()
        freq_output = run_command("sysctl -n hw.cpufrequency")
        if freq_output:
            freq_mhz = f" @ {int(freq_output.strip()) / 1000000000:.2f}GHz"
    if not cpu_name:
        cpu_name = platform.machine() or "Unknown"
    return cpu_name + freq_mhz


def detect_posix_gpu():
    output = run_command("lspci -nn | grep -Ei 'vga|3d|display' | head -n 1")
    if output:
        return output.strip()
    if platform.system() == "Darwin":
        output = run_command("system_profiler SPDisplaysDataType | grep 'Chipset Model' | head -n 1")
        match = re.search(r"Chipset Model:\s*(.+)", output)
        if match:
            return match.group(1).strip()
    return "Unknown"


def detect_posix_ram():
    output = run_command("free -m")
    match = re.search(r"Mem:\s*(\d+)", output)
    if match:
        return str(round(int(match.group(1)) / 1024 / 1024))
    if platform.system() == "Darwin":
        output = run_command("sysctl -n hw.memsize")
        match = re.search(r"(\d+)", output)
        if match:
            return str(round(int(match.group(1)) / 1024 / 1024))
    return "Unknown"


def detect_posix_storage():
    try:
        total_gb = round(shutil.disk_usage("/").total / 1024 / 1024 / 1024)
        return f"{total_gb} GiB"
    except Exception:
        return "Unknown"


platform_name = platform.system()
if platform_name == "Windows" or os.name == "nt":
    model_cpu = detect_windows_cpu()
    model_gpu = detect_windows_gpu()
    model_ram = detect_windows_ram()
    model_storages = detect_windows_storage()
else:
    model_cpu = detect_posix_cpu()
    model_gpu = detect_posix_gpu()
    model_ram = detect_posix_ram()
    model_storages = detect_posix_storage()

modeldetect_fail = any(value == "Unknown" for value in [model_cpu, model_gpu, model_ram, model_storages])

print(
    f"VoidFlan POST Checker /// v0.01a ({platform_name})\n"
    f"CPU: {model_cpu}\n"
    f"GPU: {model_gpu}\n"
    f"RAM: {model_ram} MiB\n"
    f"Storage: {model_storages}\n"
)
if modeldetect_fail:
    print("Note: Some model detection results may be unavailable on this platform.")

print("all ok")