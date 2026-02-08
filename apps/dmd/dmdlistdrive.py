#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DriveMyDisk - List
ASCII-compatible disk listing tool with color highlighting
"""

import os
import platform
import subprocess
import sys

class Colors:
    """ANSI color codes for cross-platform compatibility"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def get_disk_info():
    """
    Get disk information using system commands with better error handling
    """
    disk_info = []
    system = platform.system()

    try:
        if system == "Windows":
            # Windows system - use WMIC with improved parsing
            try:
                result = subprocess.run(
                    ['wmic', 'logicaldisk', 'get', 'size,freespace,caption,drivetype'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode != 0:
                    print(f"{Colors.YELLOW}WMIC command failed, trying alternative method...{Colors.RESET}")
                    return get_disk_info_fallback()

                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]

                for line in lines[1:]:  # Skip header
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            device = parts[0]
                            drive_type = int(parts[1])
                            free = int(parts[2]) if parts[2].isdigit() else 0
                            total = int(parts[3]) if parts[3].isdigit() else 0

                            # Only show local disks (type 3)
                            if drive_type == 3 and total > 0:
                                used = total - free
                                percent_used = (used / total) * 100 if total > 0 else 0

                                disk_info.append({
                                    'device': device + ':',
                                    'mountpoint': device + ':\\',
                                    'fstype': 'NTFS',
                                    'total': total,
                                    'used': used,
                                    'free': free,
                                    'percent_used': percent_used
                                })
                        except (ValueError, IndexError):
                            continue

            except subprocess.TimeoutExpired:
                print(f"{Colors.YELLOW}WMIC command timed out{Colors.RESET}")
                return get_disk_info_fallback()

        else:
            # Linux/Mac system - use df command
            print("do sudo then works or u dont want")
            try:
                result = subprocess.run(['sudo', 'df', '-h'], capture_output=True, text=True, timeout=10)

                if result.returncode != 0:
                    print(f"{Colors.YELLOW}DF command failed, trying alternative method...{Colors.RESET}")
                    return get_disk_info_fallback()

                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]

                for line in lines[1:]:  # Skip header
                    parts = line.split()
                    if len(parts) >= 6:
                        try:
                            device = parts[0]
                            total_str = parts[1]
                            used_str = parts[2]
                            free_str = parts[3]
                            percent_str = parts[4].replace('%', '')
                            mountpoint = parts[5]

                            # Skip virtual filesystems
                            skip_prefixes = ('/dev', '/proc', '/sys', '/run', '/snap', 'tmpfs', 'udev')
                            if any(mountpoint.startswith(prefix) for prefix in skip_prefixes):
                                continue

                            # Parse percentage
                            percent_used = int(percent_str) if percent_str.isdigit() else 0

                            disk_info.append({
                                'device': device,
                                'mountpoint': mountpoint,
                                'fstype': 'ext4',  # Default assumption
                                'total': total_str,
                                'used': used_str,
                                'free': free_str,
                                'percent_used': percent_used
                            })
                        except (ValueError, IndexError):
                            continue

            except subprocess.TimeoutExpired:
                print(f"{Colors.YELLOW}DF command timed out{Colors.RESET}")
                return get_disk_info_fallback()

    except Exception as e:
        print(f"{Colors.YELLOW}Error getting disk info: {e}{Colors.RESET}")
        return get_disk_info_fallback()

    return disk_info

def get_disk_info_fallback():
    """
    Fallback method when system commands fail
    """
    disk_info = []
    system = platform.system()

    # Simple fallback - try to detect drives by checking common paths
    if system == "Windows":
        # Check common Windows drive letters
        drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']
        for drive in drives:
            if os.path.exists(drive + '\\'):
                disk_info.append({
                    'device': drive,
                    'mountpoint': drive + ':\\',
                    'fstype': 'NTFS',
                    'total': 'Unknown',
                    'used': 'Unknown',
                    'free': 'Unknown',
                    'percent_used': 0
                })
    else:
        # Check common Unix mount points
        mount_points = ['/', '/home', '/boot', '/var']
        for mount in mount_points:
            if os.path.exists(mount):
                disk_info.append({
                    'device': 'Unknown',
                    'mountpoint': mount,
                    'fstype': 'ext4',
                    'total': 'Unknown',
                    'used': 'Unknown',
                    'free': 'Unknown',
                    'percent_used': 0
                })

    return disk_info

def format_size(size):
    """
    Format size in bytes to readable string
    """
    if isinstance(size, (int, float)):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    else:
        return str(size)

def print_disk_list():
    """
    Print ASCII-formatted disk list with color highlighting
    """
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("+===============================================================+")
    print("|               DriveMyDisk - List (ASCII Edition)              |")
    print("+===============================================================+")
    print(f"{Colors.RESET}")

    disk_info = get_disk_info()

    if not disk_info:
        print(f"{Colors.YELLOW}No disks found. This could be due to permission issues.{Colors.RESET}")
        print(f"{Colors.YELLOW}Try running as administrator/root.{Colors.RESET}")
        return

    # Print table header
    print(f"{Colors.WHITE}{Colors.BOLD}")
    print(f"{'Device':<10} {'Mount':<15} {'FS':<16} {'Total':<8} {'Used':<8} {'Free':<8} {'Use%':<6} {'Status':<8}")
    print("-" * 75)

    for i, disk in enumerate(disk_info):
        # Choose color based on usage percentage
        if disk['percent_used'] > 90:
            color = Colors.RED + Colors.BOLD
            status = "ALERT"
        elif disk['percent_used'] > 80:
            color = Colors.YELLOW
            status = "WARN"
        else:
            color = Colors.GREEN
            status = "OK"

        # Format filesystem type
        fstype = disk.get('fstype', 'N/A')
        if len(fstype) > 16:
            fstype = fstype[:16]

        # Format sizes
        total = format_size(disk['total']) if isinstance(disk['total'], (int, float)) else disk['total']
        used = format_size(disk['used']) if isinstance(disk['used'], (int, float)) else disk['used']
        free = format_size(disk['free']) if isinstance(disk['free'], (int, float)) else disk['free']

        print(f"{color}"
              f"{disk['device']:<10} {disk['mountpoint']:<15} "
              f"{fstype:<16} {total:<8} {used:<8} "
              f"{free:<8} {disk['percent_used']:>5.1f}%  {status:<8}")

    print(f"{Colors.RESET}")
    print("-" * 75)

    # Print summary statistics
    total_drives = len(disk_info)
    alert_drives = len([d for d in disk_info if d['percent_used'] > 90])
    warn_drives = len([d for d in disk_info if 80 < d['percent_used'] <= 90])
    ok_drives = total_drives - alert_drives - warn_drives

    print(f"{Colors.CYAN}Summary:{Colors.RESET}")
    print(f"  * Total Drives: {total_drives}")
    print(f"  * {Colors.GREEN}OK: {ok_drives}{Colors.RESET}")
    print(f"  * {Colors.YELLOW}Warning: {warn_drives}{Colors.RESET}")
    print(f"  * {Colors.RED}Alert: {alert_drives}{Colors.RESET}")

    # Print usage legend
    print(f"\n{Colors.CYAN}Status Tag:{Colors.RESET}")
    print(f"  {Colors.GREEN}OK{Colors.RESET}      - Usage <= 80%")
    print(f"  {Colors.YELLOW}WARNING{Colors.RESET} - Usage 80-90%")
    print(f"  {Colors.RED}ALERT{Colors.RESET}    - Usage > 90%")

def main():
    """
    Main function
    """
    try:
        print_disk_list()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Program interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Program error: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}Try running as administrator/root for full functionality.{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
