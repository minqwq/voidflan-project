import psutil
import os
import sys
import time
import platform
import datetime
import colorama
from colorama import *
import plyer
import socket
import pprint
import logging
import json

loadtime = 0

def dotLoader(howMany, howSlow):
    for dotLoader_time in range(howMany):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(howSlow)
def slowprint(text): # Byte-by-Byte to print for some effect, usage: slowprint("uwuuuuuuuuuuuuuuuuuuuu")
    for blyat in text:
        print(blyat, end="", flush=True)
        time.sleep(0.005)
    print("")
def dir_filecount(directory):
    count = 0
    for _, _, files in os.walk(directory):
        count += len(files)
        return count
def cbatteryperc():
    try:
        if psutil.sensors_battery().percent > 21:
            print(colorama.Fore.LIGHTYELLOW_EX + "[Low battery(" + str(psutil.sensors_battery().percent) + "%)]", end="")
        elif psutil.sensors_battery().percent > 11:
            print(colorama.Fore.YELLOW + "[Low battery(" + str(psutil.sensors_battery().percent) + "%)]", end="")
        elif psutil.sensors_battery().percent > 6:
            print(colorama.Fore.LIGHTRED_EX + "[Very low battery(" + str(psutil.sensors_battery().percent) + "%)]", end="")
        else:
            print("[" + str(psutil.sensors_battery().percent) + "]", end="")
    except Exception:
        pass
def linuxUtil_detectDistro():
    if platform.system() == "Linux":
        os.system("python ./apps/coreutils/tinythings/detectdistro_linux/distrodetect.py")
    else:
        platform.system()
def welcome_withDetectTime(username):
    dtn = datetime.datetime.now()
    if int(dtn.strftime("%H")) >= 6:
        print("Yo " + username + ", Good morning!")
    elif int(dtn.strftime("%H")) >= 12:
        print("It's noon " + username + ", go eat something...")
    elif int(dtn.strftime("%H")) >= 14:
        print("Good afternoon " + username + "!")
    elif int(dtn.strftime("%H")) >= 18:
        print("It's night now, still working, " + username + "?")
    elif int(dtn.strftime("%H")) >= 21:
        print("Time to sleep, " + username + ".")
    elif int(dtn.strftime("%H")) >= 0:
        print("It's overnight now, why not go to sleep " + username + "?")
def cat(file):
    try:
        tmp_catcore = open(file, "r", encoding="utf-8")
        for content in tmp_catcore:
            print(content, end="")
            time.sleep(0.01)
        print("")
    except FileNotFoundError:
        print("ERROR: file not found: " + file)
    except Exception:
        print("Unexcepted Error")
def cat_bugged(file):
    tmp_catcore = open(file, "r", encoding="utf-8")
    for content in tmp_catcore:
        print(content, end="")
        time.sleep(0.01)
    print("")
def cat_code(file): # Can be used on require-show code program, with highlight support, usage: cat_code("path/to/your/file.*")
    hlcode = highlight.highlight(file)
    print(hlcode)
def showNotify(title, message): # You can use this for desktop notify showing, usage: showNotify("title here", "uwu"), \n is available
    plyer.notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=10,
    )
def netcheck(host, port):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except OSError:
        return False
'''
Loading Spinner Stick
Usage: string, tm(string, loop_time(1 loop = 0.5s))
loading_spinner("uwu", 1)
loading_spinner("", 2)
All examples are runnable
'''
def loading_spinner(string, tm):
    try:
        for i in range(tm * 2):
            print(string + "/", end="\r")
            time.sleep(0.125)
            print(string + "-", end="\r")
            time.sleep(0.125)
            print(string + "\\", end="\r")
            time.sleep(0.125)
            print(string + "|", end="\r")
            time.sleep(0.125)
    except KeyboardInterrupt:
        pass
def filesearch(keyword, directory='.', search_subdirs=True):
    """
    Search for files and directories containing the keyword in their names
    
    :param keyword: Keyword to search for (case insensitive)
    :param directory: Directory to search in (default: current directory)
    :param search_subdirs: Whether to search subdirectories (default: True)
    :return: None (prints results directly)
    """
    # ANSI color codes
    COLOR_RESET = "\033[0m"
    COLOR_KEYWORD = "\033[1;33m"  # Bright yellow
    COLOR_FILE = "\033[0m"        # Reset (normal text)
    COLOR_DIR = "\033[1;34m"      # Bright blue
    COLOR_PATH = "\033[0;36m"     # Cyan (for paths)
    COLOR_TYPE = "\033[0;90m"     # Gray (for type indicators)

    print(f"\nSearching for '{COLOR_KEYWORD}{keyword}{COLOR_RESET}' in {COLOR_PATH}{os.path.abspath(directory)}{COLOR_RESET}\n")
    
    matches_found = False

    try:
        for root, dirs, files in os.walk(directory if search_subdirs else (directory,)):
            # Search directories first
            for dir_name in dirs:
                if keyword.lower() in dir_name.lower():
                    rel_path = os.path.relpath(root, directory)
                    display_name = dir_name.replace(
                        keyword, f"{COLOR_KEYWORD}{keyword}{COLOR_DIR}"
                    )
                    location = f"./{rel_path}" if rel_path != "." else "."
                    print(f"  {COLOR_DIR}{display_name}/{COLOR_RESET}  {COLOR_TYPE}(dir) {COLOR_PATH}({location}){COLOR_RESET}")
                    matches_found = True
            
            # Then search files
            for file_name in files:
                if keyword.lower() in file_name.lower():
                    rel_path = os.path.relpath(root, directory)
                    display_name = file_name.replace(
                        keyword, f"{COLOR_KEYWORD}{keyword}{COLOR_RESET}"
                    )
                    location = f"./{rel_path}" if rel_path != "." else "."
                    print(f"  {COLOR_FILE}{display_name}{COLOR_RESET}  {COLOR_TYPE}(file){COLOR_PATH}({location}){COLOR_RESET}")
                    matches_found = True

        if not matches_found:
            print(f"  No files or directories containing '{COLOR_KEYWORD}{keyword}{COLOR_RESET}' were found")
    
    except FileNotFoundError:
        print(f"  Error: Directory {COLOR_PATH}{directory}{COLOR_RESET} does not exist")
    except PermissionError:
        print(f"  Error: No permission to access {COLOR_PATH}{directory}{COLOR_RESET}")
def visuallog(string, level): # Logger that's can be used on your third-party program, usage:visuallog("your string", 1)
    LOG_FORMAT = '[Kernel][%(levelname)s] %(asctime)s | %(message)s'
    logging.basicConfig(filename='cache/.output.log', datefmt='%b %a %d %H:%M:%S %Y', level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger(__name__)
    if level == 0:
        print("[INFO] " + string)
        logger.info(string)
    elif level == 1:
        print(colorama.Fore.LIGHTYELLOW_EX + "[WARN] " + colorama.Fore.RESET + string)
        logger.warning(string)
    elif level == 2:
        print(colorama.Fore.LIGHTRED_EX + "[ERROR] " + colorama.Fore.RESET + string)
        logger.error(string)
    elif level == 3:
        print(colorama.Fore.RED + "[FATAL] " + colorama.Fore.RESET + string)
        logger.fatal(string)
'''
mori
- Desc: used for a command "morifetchex", will fetch the system information.
usage: see code
'''
def mori(user, hostname, curpath, configfile, devconfigfile, uptime, deviceid):
    if curpath == "":
        path = os.getcwd()
    else:
        path = curpath
    
    system_version = "0.01f"
    system_codename = "Core"

    try:
        conf = open(configfile, "r", encoding="utf-8")
        devconf = open(devconfigfile, "r", encoding="utf-8")
        cJsonRead = json.load(conf)
        cDevJsonRead = json.load(devconf)
    
        # CONFIG SET START
        system_version = cDevJsonRead["system_version"] # 版本号 / Version
        system_codename = cDevJsonRead["system_codename"] # Codename
        system_build = cDevJsonRead["system_build"] # 每做一个修改或增减内容，就加一个 Build / If changed a feature, build +=1
        system_is_beta = False # 是否为 Beta 版 / Beta version
        isWindows = cJsonRead["isWindows"] # 是否为 Windows / Are you windows?
        cmd_theme = cJsonRead["cmd_theme"] # 终端 Shell 主题 / Terminal shell theme
        isDev = False # 是否为 Dev 模式 / Dev mode
        enable_instant_show_time = cJsonRead["enable_instant_show_time"] # INstant show time before shell
        isUnregistered = cJsonRead["isUnregistered"] # Fake unregistered warning
        beep_when_finished = cJsonRead["beep_when_finished"] # When a command finished running, speaker will beep
        auto_boot_choice = cJsonRead["auto_boot_choice"] # When have a number, the boot manager will auto boot to selected operating system.
        enablePassword = cJsonRead["enablePassword"] # Enable password when login, string on the config.
        show_password_when_typing = cJsonRead["show_password_when_typing"] # Enable will not shown password when typing.
        pwdstring = cJsonRead["pwdstring"] # Password string
        allowShowNotify = cJsonRead["allowShowNotify"] # Enable to show notify in linux desktop or windows 10+
        dualBoot = cJsonRead["dualBoot"] # Allow you to boot another fake os written in any language
        dualBoot_startupCommand = cJsonRead["dualBoot_startupCommand"] # Dual boot startup command
        dualBoot_OSName = cJsonRead["dualBoot_OSName"] # Dual boot name(show in boot manager)
        venvEnable = cJsonRead["venvEnable"] # Enable python venv here
        if venvEnable == "true":
            venvPath = cJsonRead["venvPath"] # If you are linux distro, like me, you need this
        replace_python_command_to_python3 = cJsonRead["replace_python_command_to_python3"] # Replace python command to python3(when you using linux distro)
        disablePathShow = cJsonRead["disablePathShow"] # Disable path show on shell
        shorter_welcome = cJsonRead["shorter_welcome"] # Show shorter welcome text when logon
        faster_startup = cJsonRead["faster_startup"] # New version of startup screen
        rsyscmd_when_cnf = cJsonRead["rsyscmd_when_cnf"] # Run system command when command not found
    except Exception:
        print("It seems like config files are not found.")
    
    def final_prints():
        print(f"{Fore.LIGHTCYAN_EX}morifetch{Fore.LIGHTRED_EX}EX{Style.RESET_ALL} Version 1.00a\n",
              f" {Fore.YELLOW}User & Hostname: {Style.RESET_ALL}{user} at {hostname}\n",
              f" {Fore.YELLOW}Uptime: {Style.RESET_ALL}{uptime}\n",
              f" {Fore.YELLOW}Version & Codename: {Style.RESET_ALL}{system_version} \"{system_codename}\"\n",
              f" {Fore.YELLOW}Device UUID: {Style.RESET_ALL}{deviceid}\n\n"
              f"  {Fore.GREEN}Host System Release: {Style.RESET_ALL}{platform.system()} {platform.release()} {platform.version()}\n",
              f" {Fore.GREEN}Host Arch: {Style.RESET_ALL}{platform.machine()}\n\n",
              f" {Fore.CYAN}CPU: {Style.RESET_ALL}Failed to Fetch\n"
              f"  {Fore.CYAN}Native Memory: {Style.RESET_ALL}1024 KiB")
        formemcount = 0
        formemtotal = int(psutil.virtual_memory().total / 1024 / 1024)
        formemtotalkib = int(psutil.virtual_memory().total / 1024)
        for i in range(formemtotal):
            formemcount += 1
            print(f"  {Fore.CYAN}Extended Memory: {Style.RESET_ALL}{formemcount} MiB", end="\r") 
            time.sleep(0.00001)
        print(f"  {Fore.CYAN}Extended Memory: {Style.RESET_ALL}{formemtotal} MiB / {formemtotalkib} KiB")

    final_prints()

def timeformat(sectime):
    days = sectime // (24 * 3600)
    sectime %= (24 * 3600)
    hours = sectime // 3600
    sectime %= 3600
    minutes = sectime // 60
    sectime %= 60

    parts = []
    if days > 0:
        parts.append(f"{int(days)}d")
    if hours > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0:
        parts.append(f"{int(minutes)}m")
    if sectime > 0 or not parts:
        parts.append(f"{int(sectime)}s")

    return " ".join(parts)

def coresh():
    pprint.pprint(dict(globals()))
    print("End of current loaded modules.\nStarting shell...")
    print("! You are now running VoidFlan Project in Kernel mode\n"+
          "If all are dont, type \"exit\" to exit shell.")
    while True:
        cmd = input("kn >_ $ ")
        if cmd == "about":
            sk_act_about()
        elif cmd == "exit":
            sys.exit()
        elif cmd == "mori":
            mori("Scarlet Kernel II", "127.0.0.1", "/", "", "", "Unknown", "11111111-1111-1111-1111111111111111")
        elif cmd.startswith("dlt"):
            dotLoader(50, 0.01)
        else:
            print("command not found in scarlet kernel.")
