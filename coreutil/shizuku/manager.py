"""
@ PY OS Improved
@ Shizuku Software Manager
@ Shizuku Application Package Installer Core Module
@ Author: ElofHew
@ Version: 2.0
@ Date: 2025.05.02
"""

import os       # 用于操作系统交互，如获取当前目录、创建目录和删除文件等
import sys      # 用于与Python解释器交互，如退出程序等
import subprocess # 用于在Python脚本中运行外部命令
import zipfile  # 用于处理ZIP文件的压缩和解压缩
import time     # 用于添加延迟
import json     # 用于处理JSON文件的读取和写入
import shutil   # 用于文件和目录的高级操作，如复制文件和删除文件夹等
from platform import system as pfs # 用于获取当前操作系统类型
from platform import python_version as pv # 用于获取当前Python版本
from colorama import Fore, Style, init # 用于控制终端输出的颜色
import traceback # 错误报告

init(autoreset=True) # 初始化颜色模块

pyosi_path = os.getcwd()
os_type = pfs().lower()
python_ver = pv()
szk_install_path = os.path.join(pyosi_path, "data", "apps")
if not os.path.exists(szk_install_path):
    os.makedirs(szk_install_path)

def tips():
    print(f"{Fore.LIGHTGREEN_EX}% Shizuku Package Manager II %{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}==========================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}install <path> - Install a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}remove <pkg>   - Remove a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}list           - List all installed packages{Style.RESET_ALL}")
    print(f"{Fore.CYAN}credits        - See who made shizuku package manager{Style.RESET_ALL}")
    print(f"{Fore.CYAN}run <pkg>      - Run a extprog (not shizuku package){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}szk            - Run a installed shizuku package{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}search         - Search for a package (Coming soon...){Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}Shizuku has 'super' scarlet powew, isn't that just adowable? >.<{Fore.RESET}")

def run(*aargs):
    __usage__ = "Usage: shizuku run <pkg>"
    if len(aargs) < 1:
        print(f"{Fore.YELLOW}{__usage__}{Style.RESET_ALL}")
        return
    if len(aargs) == 1:
        if aargs[0] == "":
            print(f"{Fore.YELLOW}{__usage__}{Style.RESET_ALL}")
            return 1
        pkg_name = aargs[0]
        args = []
    else:
        pkg_name = aargs[0]
        args = aargs[1:]
    # Check if app exists
    app_dir_path = os.path.join(szk_install_path, pkg_name)
    try:
        # 3rd party apps
        third_party_app_list = os.path.join(pyosi_path, "data", "apps", "apps.json")
        # Open json files
        with open(third_party_app_list, "r") as tpapp_file:
            tpapp_list = json.load(tpapp_file)
        # Check command
        if pkg_name in tpapp_list:
            app_path = tpapp_list.get(pkg_name)["path"]
            if os.path.exists(app_path):
                app_file = os.path.join(app_path, "main.py")
                if not os.path.isfile(app_file):
                    print(f"{Fore.RED}Error: {app_file} not found.{Style.RESET_ALL}")
                    return 1
            else:
                print(f"{Fore.RED}Error: {app_path} not found.{Style.RESET_ALL}")
                return 1
            boot_string = str(os.path.join(pyosi_path, app_file))
            # Check arguments
            boot_args = args if args else []
            # Run app
            os.chdir(app_path)
            print("SYS.EXEC=" + sys.executable)
            process = subprocess.run([sys.executable, boot_string] + boot_args)
            if process.returncode != 0:
                print(f"{Fore.YELLOW}WARNING: This app returned a code: {process.returncode}.{Style.RESET_ALL}")
            os.chdir(pyosi_path)
            return 0
        else:
            print(f"{Fore.RED}Error: Package '{pkg_name}' not found.{Style.RESET_ALL}")
            return 1
    except FileNotFoundError:
        print(f"{Fore.RED}Info file not found.{Style.RESET_ALL}")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {pkg_name}. {e}{Style.RESET_ALL}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {pkg_name}. {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    finally:
        os.chdir(pyosi_path)

def install(*aargs):
    __usage__ = "Usage: shizuku install <package_path>"
    if not aargs or len(aargs) > 1 or aargs[0] == "":
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    pkg_path = aargs[0]
    # Main
    ins_pkg_path = os.path.abspath(pkg_path)
    temp_path = os.path.join(pyosi_path, "data", "temp")
    apps_path = os.path.join(pyosi_path, "data", "apps")

    try:
        # Check if package exists
        if not os.path.exists(ins_pkg_path):
            if not os.path.exists(os.path.abspath(pkg_path)):
                print(f"{Fore.RED}Package not found.{Fore.RESET}")
            return 1
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        if not os.path.exists(apps_path):
            os.makedirs(apps_path)

        # Extract package
        print(f"{Fore.CYAN}Installing package...{Fore.RESET}")
        extra_path = os.path.join(temp_path)
        if os.path.exists(extra_path):
            shutil.rmtree(extra_path)
        os.makedirs(extra_path)
        with zipfile.ZipFile(ins_pkg_path, "r") as zip_ref:
            zip_ref.extractall(extra_path)
    except FileNotFoundError:
        print(f"{Fore.RED}Package file not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during package check: {e}{Fore.RESET}")
        traceback.print_exception(e, limit=1145, file=sys.stdout)
        return 1
    
    # Get app name and version
    try:
        with open(os.path.join(extra_path, "info.json"), "r") as app_json_f:
            app_json = json.load(app_json_f)
            app_name = app_json["name"]
            app_version = app_json["version"]
            app_vcode = app_json["vcode"] # what is vcode? --minqwq
            app_author = app_json["author"]
            app_desc = app_json["description"]
            app_category = app_json["category"]
            app_min = app_json["min_python_version"]
            app_tar = app_json["target_python_version"]
            app_comptb = app_json["compatible_os"]
        while True:
            check = str(input(f"{Fore.CYAN}Do you want to install the package '{app_name}'? (y/n): {Fore.RESET}"))
            if check == "y" or check == "Y":
                break
            elif check == "n" or check == "N":
                print(Fore.RED + "Operation cancelled." + Fore.RESET)
                return 1
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Fore.RESET)
                continue
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        shutil.rmtree(extra_path)
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'info.json' not found.{Fore.RESET}")
        shutil.rmtree(extra_path)
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        shutil.rmtree(extra_path)
        traceback.print_exception(e, limit=1145, file=sys.stdout)
        return 1

    # Install app
    # Check the most compatible items
    try:
        if app_comptb.lower() != os_type.lower():
            print(f"{Fore.YELLOW}WARN: This app may be not compatible with your system.{Fore.RESET}")
        if int(app_min.split(".")[1]) > int(python_ver.split(".")[1]):
            print(f"{Fore.YELLOW}WARN: This app requires Python {app_min} or higher, but your Python version is {python_ver}.{Fore.RESET}")
        if int(app_tar.split(".")[1]) != int(python_ver.split(".")[1]):
            print(f"{Fore.YELLOW}WARN: This app may not work properly with your Python version.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while checking compatibility: {e}{Fore.RESET}")
        return 1

    # Check if app already exists
    try:
        app_dir = os.path.join(apps_path, app_name)
        print("APPDIR=" + app_dir.replace("/", Fore.GREEN + "/" + Fore.YELLOW))
        if os.path.exists(app_dir):
            with open(os.path.join(app_dir, "info.json"), "r") as exist_app_json_f:
                exist_app_json = json.load(exist_app_json_f)
                print("EXIST_APP_JSON=" + str(exist_app_json))
            # Same version, reinstall ask
            if exist_app_json["vcode"] == app_vcode:
                print(f"{Fore.YELLOW}Package '{app_name}' already installed. Do you want to install it again? (y/n){Fore.RESET}")
            # Higher version, downgrade ask
            elif exist_app_json["vcode"] > app_vcode:
                print(f"{Fore.YELLOW}There is a newer version of package '{app_name}'. Would you like to downgrade it? (y/n){Fore.RESET}")
            # Lower version, upgrade ask
            elif exist_app_json["vcode"] < app_vcode:
                print(f"{Fore.YELLOW}There is an older version of package '{app_name}'. Would you like to upgrade it? (y/n){Fore.RESET}")
            else:
                print(f"{Fore.RED}An error occurred while checking package '{app_name}'.{Fore.RESET}")
                return 1
            while True:
                check = str(input("> "))
                if check == "y" or check == "Y":
                    break
                elif check == "n" or check == "N":
                    print(Fore.RED + "Operation cancelled." + Fore.RESET)
                    return 0
                else:
                    print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Fore.RESET)
                    continue
            # Remove old app directory
            shutil.rmtree(app_dir)
        # Copy app files to app directory
        shutil.copytree(extra_path, app_dir)
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        return 0
    except FileExistsError:
        print(f"{Fore.RED}Directory '{app_name}' already exists.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during package installation: {e}{Fore.RESET}")
        traceback.print_exception(e, limit=1145, file=sys.stdout)
        return 1

    # Install dependencies
    try:
        if os.path.isfile(os.path.join(extra_path, "requirements.txt")):
            print(f"{Fore.CYAN}Installing dependencies...{Fore.RESET}")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(extra_path, "requirements.txt")], check=True)
        else:
            print(f"{Fore.YELLOW}No dependencies found.{Fore.RESET}")
    except FileNotFoundError:
        print(f"{Fore.RED}File 'info.json' in app directory not found.{Fore.RESET}")
        return 1
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        return 0
    except json.JSONDecodeError:
        print(f"{Fore.RED}File 'info.json' format is incorrect.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1

    # Add app to registry
    try:
        if not os.path.exists(os.path.join(pyosi_path, "data", "apps")):
            os.makedirs(os.path.join(pyosi_path, "data", "apps"))
        apps_json_path = os.path.join(pyosi_path, "data", "apps", "apps.json")
        if os.path.exists(apps_json_path):
            with open(apps_json_path, "r") as add_app_f:
                add_app_config = json.load(add_app_f)
        else:
            add_app_config = {}
        add_app_config[app_name] = {
            "path": app_dir if not app_dir.startswith(pyosi_path) else app_dir.replace(pyosi_path, "."),
            "version": app_version,
            "version_code": app_vcode,
            "author": app_author,
            "description": app_desc,
            "category": app_category,
            "min_python_version": app_min,
            "target_python_version": app_tar,
            "comptb_os": app_comptb,
        }
        with open(apps_json_path, "w") as add_app_f:
            json.dump(add_app_config, add_app_f, indent=4)
        print(f"{Fore.GREEN}Package '{app_name}' has been successfully installed.{Fore.RESET}")
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during app registry update: {e}{Fore.RESET}")
        traceback.print_exception(e, limit=1145, file=sys.stdout)
        return 1
    
    # Clean up
    try:
        shutil.rmtree(extra_path)
        return 0
    except Exception as e:
        print(f"{Fore.RED}An error occurred during cleanup: {e}{Fore.RESET}")
        traceback.print_exception(e, limit=1145, file=sys.stdout)
        return 1

def remove(*aargs):
    __usage__ = "Usage: shizuku remove <package>"
    if not aargs or len(aargs) > 1 or aargs[0] == "":
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    app_name = aargs[0]
    # Check if app exists in registry
    print(f"{Fore.RED}Removing package: {app_name}{Fore.RESET}")
    # Confirm removal
    while True:
        try:
            check = str(input(f"{Fore.CYAN}Do you want to remove the package '{app_name}'? (y/n): {Fore.RESET}"))
            if check == "y" or check == "Y":
                break
            elif check == "n" or check == "N":
                print(Fore.RED + "Operation cancelled." + Fore.RESET)
                return 1
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Fore.RESET)
                continue
        except KeyboardInterrupt:
            print(Fore.RED + "Operation cancelled." + Fore.RESET)
            return 0

    # Check app registry
    try:
        apps_json_path = os.path.join(pyosi_path, "data", "apps", "apps.json")
        with open(apps_json_path, "r") as add_app_f:
            add_app_config = json.load(add_app_f)
        if app_name in add_app_config:
            app_dir = add_app_config[app_name]["path"]
            if not os.path.isabs(app_dir):
                app_dir = os.path.join(pyosi_path, app_dir)
        else:
            print(f"{Fore.YELLOW}Package '{app_name}' not found. No need to remove.{Fore.RESET}")
            return 1
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
    
    # Remove app directory
    try:
        shutil.rmtree(app_dir)
        with open(apps_json_path, "r") as add_app_f:
            add_app_config = json.load(add_app_f)
        del add_app_config[app_name]
        with open(apps_json_path, "w") as add_app_f:
            json.dump(add_app_config, add_app_f, indent=4)
        print(f"{Fore.GREEN}Package '{app_name}' has been successfully removed.{Fore.RESET}")
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}Directory '{app_name}' not found.{Fore.RESET}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}An error occurred during directory removal: {e}{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during removal: {e}{Fore.RESET}")
        return 1

def list_apps():
    # Main
    try:
        apps_json_path = os.path.join(pyosi_path, "data", "apps", "apps.json")
        if os.path.exists(apps_json_path):
            with open(apps_json_path) as add_app_f:
                add_app_config = json.load(add_app_f)
        else:
            add_app_config = {}
        if len(add_app_config) == 0:
            print(f"{Fore.YELLOW}No packages installed.{Fore.RESET}")
            return 1
        else:
            all_app_list = {**add_app_config}
            print(f"{Fore.GREEN}Installed packages:{Fore.RESET}")
            print(f"{Fore.CYAN}[Name]{Fore.RESET} - {Fore.GREEN}[Version]{Fore.RESET} - {Fore.LIGHTBLUE_EX}[Author]{Fore.RESET} - {Fore.YELLOW}[Category]{Fore.RESET} - {Fore.LIGHTMAGENTA_EX}[Description]{Style.RESET_ALL}")
            for app_name in all_app_list:
                app_version = all_app_list[app_name]["version"]
                app_author = all_app_list[app_name]["author"]
                app_desc = all_app_list[app_name]["description"]
                app_category = all_app_list[app_name]["category"]
                print(f"{Fore.CYAN}{app_name}{Fore.RESET} - {Fore.GREEN}{app_version}{Fore.RESET} - {Fore.LIGHTBLUE_EX}{app_author}{Fore.RESET} - {Fore.YELLOW}{app_category}{Fore.RESET} - {Fore.LIGHTMAGENTA_EX}{app_desc}{Fore.RESET}")
            return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.\n{Fore.CYAN}Looks like you haven't installed any packages yet.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
