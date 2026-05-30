# subprocess_restart.py
import sys
import os
import subprocess
import time
import signal
import atexit

def restart_via_subprocess():
    """
    通过创建新子进程来重启当前脚本
    这会启动全新的Python进程
    """
    print("\n正在通过子进程重启...")

    # 获取当前脚本路径
    script_path = os.path.abspath(__file__)

    # 获取当前Python解释器
    python_exe = sys.executable

    # 获取当前命令行参数
    args = sys.argv

    # 构建新命令
    cmd = [python_exe, script_path] + args[1:]

    print(f"重启命令: {' '.join(cmd)}")

    # 启动新进程
    try:
        # 使用Popen启动新进程
        new_process = subprocess.Popen(
            cmd,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env=os.environ.copy()
        )

        print(f"新进程PID: {new_process.pid}")

        # 退出当前进程
        print("退出当前进程...")
        sys.exit(0)

    except Exception as e:
        print(f"重启失败: {e}")
        return False

# 状态保持示例
class AppState:
    """应用程序状态"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.start_time = time.time()
            cls._instance.restart_count = 0
            cls._instance.data = {}
        return cls._instance

    def increment_counter(self):
        self.restart_count += 1

    def get_info(self):
        return {
            'uptime': time.time() - self.start_time,
            'restarts': self.restart_count,
            'data': self.data.copy()
        }

def main():
    """主函数"""
    # 获取或创建应用状态
    app_state = AppState()
    app_state.increment_counter()

    state_info = app_state.get_info()

    print(
        "\n=================================================="
        "\nPython脚本重启演示"
        "\n=================================================="
        f"\n启动时间: {time.ctime(app_state.start_time)}"
        f"\n运行时间: {state_info['uptime']:.2f}秒"
        f"\n重启次数: {state_info['restarts']}"
        f"\n当前时间: {time.ctime()}"
        f"\n进程PID: {os.getpid()}"
        "\n=================================================="
    )

    # 业务逻辑
    for i in range(3):
        print(f"处理任务 {i+1}/3...")
        time.sleep(1)

    # 用户交互
    print(
        "\n可用命令:"
        "\n  1 - 查看状态"
        "\n  2 - 修改数据"
        "\n  3 - 重启脚本"
        "\n  0 - 退出"
    )

    while True:
        try:
            choice = "3" # input("\n请输入选择 (0-3): ").strip()

            if choice == '1':
                info = app_state.get_info()
                print(f"当前状态: {info}")

            elif choice == '2':
                key = input("请输入数据键: ").strip()
                value = input("请输入数据值: ").strip()
                app_state.data[key] = value
                print(f"已设置 {key} = {value}")

            elif choice == '3':
                confirm = "y" # input("确认重启？(y/n): ").strip().lower()
                if confirm == 'y':
                    restart_via_subprocess()
                else:
                    print("取消重启")

            elif choice == '0':
                print("退出程序")
                break

            else:
                print("无效选择")

        except KeyboardInterrupt:
            print("\n接收到中断信号")
            break
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # 注册退出清理
    atexit.register(lambda: print(f"\n进程 {os.getpid()} 退出"))

    # 运行主函数
    main()
