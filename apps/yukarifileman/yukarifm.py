import os
import shutil
import sys
import colorama

def run_file_manager():
    cwd = os.getcwd()

    def list_dir():
        for name in os.listdir(cwd):
            path = os.path.join(cwd, name)
            if os.path.isdir(path):
                print(f"[{colorama.Fore.YELLOW}DIR{colorama.Style.RESET_ALL}]  {colorama.Fore.YELLOW}{name}{colorama.Style.RESET_ALL}/")
            else:
                print(f"[{colorama.Fore.CYAN}FILE{colorama.Style.RESET_ALL}] {colorama.Fore.CYAN}{name}{colorama.Style.RESET_ALL}")

    print("YukariFM v0.01a 体验版 Plus")
    print("Type HELP for commands\n")

    while True:
        try:
            cmd = input(f"{cwd}> ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            head = parts[0].upper()

            if head in ("EXIT", "QUIT"):
                return

            elif head in ("CLS", "CLEAR"):
                os.system("cls" if os.name == "nt" else "clear")

            elif head in ("DIR", "LS"):
                list_dir()

            elif head == "PWD":
                print(cwd)

            elif head == "CD":
                if len(parts) < 2:
                    continue
                target = os.path.abspath(os.path.join(cwd, parts[1]))
                if os.path.isdir(target):
                    cwd = target
                    os.chdir(cwd)
                else:
                    print("Directory not found")

            elif head in ("MD", "MKDIR"):
                if len(parts) < 2:
                    continue
                os.mkdir(os.path.join(cwd, parts[1]))

            elif head in ("RD", "RMDIR"):
                if len(parts) < 2:
                    continue
                os.rmdir(os.path.join(cwd, parts[1]))

            elif head == "TYPE":
                if len(parts) < 2:
                    continue
                path = os.path.join(cwd, parts[1])
                if os.path.isfile(path):
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        print(f.read())
                else:
                    print("Not a file")

            elif head == "COPY":
                if len(parts) < 3:
                    continue
                shutil.copy2(
                    os.path.join(cwd, parts[1]),
                    os.path.join(cwd, parts[2])
                )

            elif head == "DEL":
                if len(parts) < 2:
                    continue
                os.remove(os.path.join(cwd, parts[1]))

            elif head == "HELP":
                print("""
Commands:
  DIR / LS       List files
  CD <dir>       Change directory
  MD / MKDIR     Make directory
  RD / RMDIR     Remove empty directory
  TYPE <file>    Show file content
  COPY src dst   Copy file
  DEL <file>     Delete file
  PWD            Show current path
  CLS / CLEAR    Clear screen
  EXIT           Exit file manager
""")

            else:
                print("Bad command or filename")

        except Exception as e:
            print(f"Error: {e}")


# 关键：只有直接运行才启动
if __name__ == "__main__":
    run_file_manager()