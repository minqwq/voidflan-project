"""
@ name: Leaf Boot Manager
@ author: ElofHew
@ date: 2025-07-18
@ version: 1.0
@ license: GNU General Public License v3.0
@ copyright: (c) 2025 Oak Studio. All rights reserved.
@ description: This is a Boot Manager for Python Fake Operating Systems.
"""

import os
import sys
import time
import json
import shutil
import platform
import subprocess
from pathlib import Path
from colorama import Fore, Style, Back
from colorama import init as cinit

cinit(autoreset=True)

# 定义全局变量
boot_path = os.path.dirname(os.path.abspath(__file__))
os_type = platform.system()

terminal_width = shutil.get_terminal_size().columns
terminal_height = shutil.get_terminal_size().lines

lbm_path = "./.lbm"
lbm_error_log = os.path.join(lbm_path, "logs", "error.log")

def cs(): os.system("cls" if os_type == "Windows" else "clear")

class Actions:
    """定义操作类"""
    def __init__(self):
        pass

    def shutdown(self):
        cs()
        sys.exit(0)

    def st_with_error(self, error_code=1):
        input("(Press Enter to shutdown...)")
        cs()
        if isinstance(error_code, int):
            sys.exit(error_code)
        else:
            sys.exit(1)

    def reboot(self):
        cs()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()

    def rb_with_error(self):
        input("(Press Enter to reboot...)")
        cs()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()

    def rb_to_rec(self):
        input("(Press Enter to reboot to recovery mode...)")
        cs()
        subprocess.call([sys.executable, sys.argv[0]])
        sys.exit()

class BootSystem:
    """定义系统启动类"""
    def __init__(self, data_list):
        # 使用更安全的字典获取方法
        self.name = data_list.get("name", "VoidFlan Project") if isinstance(data_list, dict) else "Unknown System"
        self.ename = data_list.get("ename", "vfp") if isinstance(data_list, dict) else "unknown"
        self.version = data_list.get("version", "2.0 Beta 3") if isinstance(data_list, dict) else "Unknown"
        self.vercode = data_list.get("vercode", "2003") if isinstance(data_list, dict) else "0000"
        self.setup_date = data_list.get("setup_date", "1970-01-01") if isinstance(data_list, dict) else "1970-01-01"
        self.need_venv = data_list.get("need_venv", "false") if isinstance(data_list, dict) else "false"
        self.min_python = data_list.get("min_python", "3.8") if isinstance(data_list, dict) else "3.8"
        self.support_os = data_list.get("support_os", ["windows", "nt", "posix", "unix", "macos", "osx", "linux"]) if isinstance(data_list, dict) else ["windows", "linux"]
        self.boot_class = data_list.get("boot_class", "idk") if isinstance(data_list, dict) else "system"
        self.work_file = data_list.get("work_file", "voidflan.py") if isinstance(data_list, dict) else "main.py"
        self.work_path = data_list.get("work_path", ".") if isinstance(data_list, dict) else "."

    # 启动主函数
    def main(self):
        try:
            # 检查该伪系统的路径是否存在
            check_os_path_result = self.check_os_path()
            if check_os_path_result != 0:
                return 1
            # 检查父操作系统是否受支持
            check_support_os_result = self.check_support_os()
            if check_support_os_result != 0:
                return 1
            # 检查Python版本是否满足最低要求
            check_python_version_result = self.check_python_version()
            if check_python_version_result == 1:
                return 1
            # 检查是否需要虚拟环境
            self.venv_path_result = self.check_venv()
            if self.venv_path_result == 1:
                return 1
            # 启动系统
            start_system_result = self.start_system()
            return start_system_result
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            return 1
        finally:
            os.chdir(boot_path)

    def check_os_path(self):
        try:
            full_work_path = os.path.join(boot_path, self.work_path)
            full_work_file = os.path.join(full_work_path, self.work_file)

            if not os.path.exists(full_work_path):
                print(f"{Fore.RED}Error: System work path does not exist: {full_work_path}{Style.RESET_ALL}")
                return 1
            if not os.path.exists(full_work_file):
                print(f"{Fore.RED}Error: System work file does not exist: {full_work_file}{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check path. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_support_os(self):
        try:
            if os_type.lower() not in [os.lower() for os in self.support_os]:
                print(f"{Fore.RED}Error: This system ({os_type}) is not supported by this Fake Operating System.{Style.RESET_ALL}")
                return 1
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check support OS. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_python_version(self):
        try:
            current_version = platform.python_version()
            get_version = current_version.split(".")
            imp_version = self.min_python.split(".")

            if int(imp_version[0]) == 2:
                print(f"{Fore.RED}Error: Leaf Boot Manager only supports Python 3.{Style.RESET_ALL}")
                return 1
            elif int(get_version[0]) < int(imp_version[0]):
                print(f"{Fore.RED}Error: This Fake OS need Python {self.min_python} or higher, but your system has Python {current_version}. Please upgrade your Python version.{Style.RESET_ALL}")
                return 1
            elif int(get_version[1]) < int(imp_version[1]):
                print(f"{Fore.RED}Error: This Fake OS need Python {self.min_python} or higher, but your system has Python {current_version}. Please upgrade your Python version.{Style.RESET_ALL}")
                return 1
            else:
                return 0
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check Python version. Error message: {e}{Style.RESET_ALL}")
            return 1

    def check_venv(self):
        try:
            if self.need_venv.lower() != "true":
                return 0

            venvname = self.ename.lower()
            venvs_path = os.path.join(lbm_path, "pyvenv")
            current_venv = os.path.join(venvs_path, venvname)

            if os_type == "Windows":
                executable_path = os.path.join(current_venv, "Scripts", "python.exe")
            else:
                executable_path = os.path.join(current_venv, "bin", "python")

            if not os.path.exists(executable_path):
                print(f"{Fore.YELLOW}WARNING: Virtual environment {venvname} does not exist. Creating...{Style.RESET_ALL}")
                if os.path.exists(current_venv):
                    shutil.rmtree(current_venv)

                if not os.path.exists(venvs_path):
                    os.makedirs(venvs_path)

                os.chdir(venvs_path)
                make_venv = subprocess.run([sys.executable, "-m", "venv", venvname])
                if make_venv.returncode != 0:
                    print(f"{Fore.RED}Error: Failed to create virtual environment {venvname}.{Style.RESET_ALL}")
                    return 1

            self.venv_exec = executable_path
            return 0
        except Exception as e:
            # 修复：在异常处理中安全地获取venvname
            venvname = getattr(self, 'ename', 'unknown').lower()
            print(f"{Fore.RED}Error: Failed to create virtual environment {venvname}. Error message: {e}{Style.RESET_ALL}")
            return 1
        finally:
            os.chdir(boot_path)

    def start_system(self):
        try:
            # 准备启动专用的参数
            if self.boot_class == "system":
                boot_arg = ["--boot", "--regular"]
            elif self.boot_class == "recovery":
                boot_arg = ["--boot", "--recovery"]
            else:
                boot_arg = []

            # 准备系统工作路径和主文件名
            work_path = os.path.join(boot_path, self.work_path)
            work_file = self.work_file

            # 根据是否需要虚拟环境来决定使用的Python解释器
            if self.need_venv.lower() == "true":
                if not hasattr(self, 'venv_exec'):
                    print(f"{Fore.RED}Error: Virtual environment not properly configured.{Style.RESET_ALL}")
                    return 1
                pyexec = self.venv_exec
            else:
                pyexec = sys.executable

            # 正式启动系统
            os.chdir(work_path)
            system_process = subprocess.run([pyexec, work_file] + boot_arg)

            # 获取该伪系统的返回码并返回到上层
            return system_process.returncode
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to start system. Error message: {e}{Style.RESET_ALL}")
            return 1

class CheckSystem:
    """定义系统文件检查类"""
    def __init__(self):
        self.check_lbm_directory()
        self.check_system_file()

    def check_lbm_directory(self):
        """检查并创建Leaf Boot Manager的必要目录"""
        try:
            if not os.path.exists(lbm_path):
                os.makedirs(lbm_path)
            logs_path = os.path.join(lbm_path, "logs")
            if not os.path.exists(logs_path):
                os.makedirs(logs_path)
            venvs_path = os.path.join(lbm_path, "pyvenv")
            if not os.path.exists(venvs_path):
                os.makedirs(venvs_path)
        except Exception as e:
            print(f"{Fore.RED}Error: Have some problems when creating directories. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)

    def check_system_file(self):
        """检查系统文件是否存在"""
        try:
            system_file_path = "lsystem.json"
            if not os.path.exists(system_file_path):
                # 创建默认的系统文件
                default_systems = {
                    "1": {
                        "name": "VoidFlan Project",
                        "ename": "vfp",
                        "version": "2.0 Beta 3",
                        "vercode": "2003",
                        "setup_date": "2024-01-01",
                        "need_venv": "false",
                        "min_python": "3.8",
                        "support_os": ["windows", "linux", "darwin"],
                        "boot_class": "system",
                        "work_file": "voidflan.py",
                        "work_path": "."
                    }
                }
                with open(system_file_path, "w", encoding="utf-8") as f:
                    json.dump(default_systems, f, indent=4, ensure_ascii=False)
                print(f"{Fore.YELLOW}Created default system configuration file: {system_file_path}{Style.RESET_ALL}")
            else:
                # 检查现有文件格式是否正确
                with open(system_file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    # 如果文件内容看起来像是单个系统配置而不是系统列表
                    if content.startswith('{') and not content.startswith('{"1":'):
                        print(f"{Fore.YELLOW}WARNING: System file format is incorrect. Fixing...{Style.RESET_ALL}")
                        # 读取单个系统配置
                        single_system = json.loads(content)
                        # 转换为正确的格式
                        corrected_systems = {"1": single_system}
                        with open(system_file_path, "w", encoding="utf-8") as f:
                            json.dump(corrected_systems, f, indent=4, ensure_ascii=False)
                        print(f"{Fore.GREEN}Fixed system file format{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to check system file. Error message: {e}{Style.RESET_ALL}")
            sys.exit(1)

def get_return_code(return_code=None):
    """根据返回值执行相应操作"""
    try:
        # 根据返回值执行相应操作
        if return_code is None:
            print(f"{Fore.RED}Error: No valid system was selected.{Style.RESET_ALL}")
            Actions().st_with_error(1)
        elif return_code == 0:
            # 正常关机
            Actions().shutdown()
        elif return_code == 1:
            # 启动前检查环节出错
            print(f"{Fore.RED}Error: Failed to start system. Please check the system configuration.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 11:
            # 重新启动
            Actions().reboot()
        elif return_code == 12:
            # 未完成的功能
            print(f"{Fore.YELLOW}WARNING: This Fake OS want to boot into an unfinished feature.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 13:
            # 系统启动失败
            print(f"{Fore.RED}Error: Boot Fake OS failed.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 14:
            # 系统崩溃
            print(f"{Fore.RED}Error: This Fake OS has crashed.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 15:
            # 重启至恢复模式
            Actions().rb_to_rec()
        elif return_code == 16:
            # 启动参数错误
            print(f"{Fore.RED}Error: Boot Arguments invalid.{Style.RESET_ALL}")
            Actions().rb_with_error()
        elif return_code == 17:
            # Ctrl+C被触发
            print(f"{Fore.YELLOW}WARNING: Shutdown initiated by user.{Style.RESET_ALL}")
            Actions().st_with_error(0)
        elif return_code == 19:
            # 捕捉到异常错误
            print(f"{Fore.RED}Error: This Fake OS caught an exception error.{Style.RESET_ALL}")
            Actions().rb_with_error()
        else:
            # 未知错误
            print(f"{Fore.RED}Error: Unknown error. Code: {return_code}{Style.RESET_ALL}")
            Actions().st_with_error(return_code)
    except Exception as e:
        print(f"{Fore.RED}Error: Failed to handle return code. Error message: {e}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    """主函数"""
    try:
        # 检查系统文件
        CheckSystem()

        # 读取系统启动项列表
        system_file_path = "lsystem.json"
        if not os.path.exists(system_file_path):
            print(f"{Fore.RED}Error: System file {system_file_path} not found.{Style.RESET_ALL}")
            sys.exit(1)

        with open(system_file_path, "r", encoding="utf-8") as lbm_system_file_obj:
            try:
                system_data = json.load(lbm_system_file_obj)
            except json.JSONDecodeError:
                print(f"{Fore.RED}Error: Invalid JSON format in {system_file_path}{Style.RESET_ALL}")
                sys.exit(1)

        # 验证系统数据结构
        if not isinstance(system_data, dict):
            print(f"{Fore.RED}Error: System data should be a dictionary{Style.RESET_ALL}")
            sys.exit(1)

        # 检查是否是单个系统配置而不是系统列表
        if not any(key.isdigit() for key in system_data.keys()):
            print(f"{Fore.YELLOW}WARNING: System file contains single system configuration. Converting to list format...{Style.RESET_ALL}")
            # 转换为正确的格式
            system_data = {"1": system_data}
            # 保存修正后的文件
            with open(system_file_path, "w", encoding="utf-8") as f:
                json.dump(system_data, f, indent=4, ensure_ascii=False)
            print(f"{Fore.GREEN}Fixed system file format{Style.RESET_ALL}")

        # 绘制启动菜单
        print(f"{int((terminal_width-17)/2) * ' '}{Fore.CYAN}Leaf Boot Manager{Style.RESET_ALL}{int((terminal_width-17)/2) * ' '}")
        print("=" * terminal_width)
        print(f"{Fore.LIGHTGREEN_EX}0. Shutdown{Style.RESET_ALL}")

        # 安全地遍历系统数据
        for key, value in system_data.items():
            # 检查value是否为字典
            if not isinstance(value, dict):
                print(f"{Fore.RED}{key}. Invalid system configuration{Style.RESET_ALL}")
                continue

            # 安全地获取名称和版本
            f_name = value.get("name", "VoidFlan Project II")
            f_version = value.get("version", "2.0 Beta 3")
            print(f"{Fore.LIGHTGREEN_EX}{key}. {f_name} - {f_version}{Style.RESET_ALL}")

        print("=" * terminal_width)

        return_code = None  # 初始化return_code

        # 选择启动项
        while True:
            try:
                choice = input(f"{Fore.LIGHTBLUE_EX}>>> {Style.RESET_ALL}")
                if choice == "0":
                    return_code = 0
                    break
                elif choice in system_data:
                    # 检查选择的系统配置是否有效
                    selected_system = system_data[choice]
                    if not isinstance(selected_system, dict):
                        print(f"{Fore.RED}Error: Invalid system configuration for choice {choice}{Style.RESET_ALL}")
                        continue

                    print(f"{Fore.LIGHTGREEN_EX}Starting system {selected_system.get('name', 'Unknown System')}...{Style.RESET_ALL}")
                    time.sleep(0.5)

                    # BootSystem Class
                    return_code = BootSystem(selected_system).main()
                    break
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                    continue
            except KeyboardInterrupt:
                return_code = 17
                break

        get_return_code(return_code)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    cs()
    main()
