# Main code - VoidFlan Project
print("每次重启主机系统后再次启动此程序可能需要一段时间才能初始化，请耐心等待。")
try:
    from goto import goto
except ModuleNotFoundError:
    from python_goto import goto
import ast
import json
import getpass
import os
import sys
import datetime
import colorama
import time
import traceback
import logging
import uuid
try:
    from coreutil.module.actions import *
    from coreutil.module.style import *
    from coreutil.module.textmoji import *
    from coreutil.module.splashes import *
    from coreutil.module.network import *
except Exception as crashReason:
    print(crashReason + " Can't startup currently, kernel is broken.")
    sys.exit(15)
try:
    import curses
except ModuleNotFoundError:
    print("If you are trying run this on windows, please install curses module.(you can ignore this if you dont need advanced startup screen)")
    input("[Press any key to continue...]")
import psutil
visuallog("Initialing unimportant Kernel Feature...", 0)
try:
    import coreutil.shizuku.manager as szkmng # Installer for shizuku
    import coreutil.oeminfo.printoeminfo as oeminfo
    import coreutil.module.rebootspell as rebootspell
except Exception as crashReason:
    visuallog(crashReason + ", can't to load", 2)
print("\033[?25l")

# Init defines
cmdhist_lines = 0
cmdhist_time = ""
cmd = ""
lsh_hostname = "scarletlocal-000"
user = "defaultuser-000"
lsh_path = os.getcwd()
lsh_path_fixed = os.getcwd()
networked = False
rpia_404 = False
debugMode = ""
isDevchan = False
isDev = False
logout = False
cmdhist_timed = datetime.datetime.now().strftime("%b %a %d %H:%M:%S %Y")

# Init configs
try:
    conf = open("./config/config.json", "r", encoding="utf-8")
    cmdthemeconf = open("./config/cmd_theme.json", "r", encoding="utf-8")
    devconf = open("./config/.devconfig/confdev.json", "r", encoding="utf-8")
    kiconf = open("./coreutil/module/kernelinfo.json", "r", encoding="utf-8")
    hostconf = open("./config/hostnamecfg.json", "r", encoding="utf-8")
    searcherconf = open("./config/searcher.json", "r", encoding="utf-8")
    jsonRead = json.load(conf)
    cmdThemeJsonRead = json.load(cmdthemeconf)
    devJsonRead = json.load(devconf)
    kiJsonRead = json.load(kiconf)
    hostconfJsonRead = json.load(hostconf)
    searcherconfJsonRead = json.load(searcherconf)
except json.decoder.JSONDecodeError:
    input("[JSON Syntax Incorrect] Press any key to except")
# Set logger style
LOG_FORMAT = '[Embedded][%(levelname)s] %(asctime)s | %(message)s'
logging.basicConfig(filename='cache/.output.log', datefmt='%b %a %d %H:%M:%S %Y', level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.info("Logger started successfully.")

# CONFIG START
try:
    system_version = devJsonRead["system_version"] # 版本号 / Version
    system_codename = devJsonRead["system_codename"] # Codename
    system_codename_lower = devJsonRead["system_codename_lower"] # Codename Lowercased
    system_is_beta = False # 是否为 Beta 版 / Beta version
    isWindows = jsonRead["isWindows"] # 是否为 Windows / Are you windows?
    cmd_theme = jsonRead["cmd_theme"] # 终端 Shell 主题 / Terminal shell theme
    # 是否为 Dev 频道 / Devchan
    try:
        sysdevchanSplit = system_codename_lower.split("-")[1]
        if sysdevchanSplit.startswith("dev"):
            isDevchan = True
    except IndexError:
        pass
    enable_instant_show_time = jsonRead["enable_instant_show_time"] # INstant show time before shell
    isUnregistered = jsonRead["isUnregistered"] # Fake unregistered warning
    beep_when_finished = jsonRead["beep_when_finished"] # When a command finished running, speaker will beep
    auto_boot_choice = jsonRead["auto_boot_choice"] # When have a number, the boot manager will auto boot to selected operating system.
    enablePassword = jsonRead["enablePassword"] # Enable password when login, string on the config.
    show_password_when_typing = jsonRead["show_password_when_typing"] # Enable will not shown password when typing.
    pwdstring = jsonRead["pwdstring"] # Password string
    allowShowNotify = jsonRead["allowShowNotify"] # Enable to show notify in linux desktop or windows 10+
    dualBoot = jsonRead["dualBoot"] # Allow you to boot another fake os written in any language
    dualBoot_startupCommand = jsonRead["dualBoot_startupCommand"] # Dual boot startup command
    dualBoot_OSName = jsonRead["dualBoot_OSName"] # Dual boot name(show in boot manager)
    venvEnable = jsonRead["venvEnable"] # Enable python venv here
    if venvEnable == True:
        venvPath = jsonRead["venvPath"] # If you are linux distro, like me, you need this
    replace_python_command_to_python3 = jsonRead["replace_python_command_to_python3"] # Replace python command to python3(when you using linux distro)
    disablePathShow = jsonRead["disablePathShow"] # Disable path show on shell
    shorter_welcome = jsonRead["shorter_welcome"] # Show shorter welcome text when logon
    faster_startup = jsonRead["faster_startup"] # New version of startup screen
    rsyscmd_when_cnf = jsonRead["rsyscmd_when_cnf"] # Run system command when command not found
    autoexecute_prompt_on_effects = jsonRead.get("autoexecute_prompt_on_effects", True) # Prompt before running autoexecute.py when it may modify variables or environment
    autoexecute_show_variable_changes = jsonRead.get("autoexecute_show_variable_changes", True) # Print each variable change made by autoexecute.py
    python_exec_path_windows = jsonRead["python_exec_path_windows"] # Python executable path(Windows only, linux/posix use venv instead)
    autologin_username = devJsonRead["autologin_username"]
    enable_legacy_help_engine = jsonRead["enable_legacy_help_engine"]
    expertfeature_cd_enabled = True # cd command availablity
    kernelver = kiJsonRead["version"] # Kernel version
    distribution_name = devJsonRead["distribution_name"] # 发行版名称
    whereis_searchspeed = searcherconfJsonRead["searching_speed"]
    try:
        deviceid = open(lsh_path_fixed + "/config/deviceid.txt", "r", encoding="utf-8").readline().strip()
    except Exception:
        pass
except json.decoder.JSONDecodeError:
    input("[JSON Syntax Incorrect] Press any key to except")
# HOSTNAME CONFIG START
use_ip_as_hostname = hostconfJsonRead["use_ip_as_hostname"] # Show local ip on hostname instead of custom string
disable_hostname = hostconfJsonRead["disable_hostname"] # Show nothing instead of hostname after username

if use_ip_as_hostname == True:
    lsh_hostname = network_ip.get_local_ip()
else:
    lsh_hostname = jsonRead["default_hostname"] # Your default hostname(Boot ID 1 only)
# CONFIG END

if disablePathShow == True:
    lsh_path = "DISABLED"

# core/plaintext loads START
co_manualHelp = "coreutil/plaintext/manualhelp.txt"
co_welcome = "coreutil/plaintext/welcome.txt"
# core/plaintext loads END

cmd_theme_templates = cmdThemeJsonRead.get("themes", cmdThemeJsonRead)

def build_cmd_prompt(theme_name, username, hostname, path):
    cmd_theme_template = cmd_theme_templates.get(theme_name)
    if isinstance(cmd_theme_template, dict):
        if getpass.getuser() == "root":
            cmd_theme_template = cmd_theme_template.get("root")
        else:
            cmd_theme_template = cmd_theme_template.get("normal")
    if cmd_theme_template is None:
        cmd_theme_template = cmd_theme_templates.get("default")
    if cmd_theme_template is None:
        cmd_theme_template = "{light_blue}{user}{grey}:{cyan}{hostname}{light_green} > {reset}"
    return cmd_theme_template.format(
        user=username,
        hostname=hostname,
        path=path,
        blue=colorama.Fore.LIGHTBLUE_EX,
        cyan=colorama.Fore.LIGHTCYAN_EX,
        green=colorama.Fore.LIGHTGREEN_EX,
        light_blue=colorama.Fore.LIGHTBLUE_EX,
        light_cyan=colorama.Fore.LIGHTCYAN_EX,
        light_green=colorama.Fore.LIGHTGREEN_EX,
        light_yellow=colorama.Fore.LIGHTYELLOW_EX,
        light_red=colorama.Fore.LIGHTRED_EX,
        light_magenta=colorama.Fore.LIGHTMAGENTA_EX,
        light_white=colorama.Fore.LIGHTWHITE_EX,
        red=colorama.Fore.LIGHTRED_EX,
        yellow=colorama.Fore.LIGHTYELLOW_EX,
        magenta=colorama.Fore.LIGHTMAGENTA_EX,
        grey=color.grey,
        reset=color.reset,
    )

def cmdhistory_write():
    tmp_f = open("cache/history.txt", "a", encoding="utf-8")
    # cmdhist_lines += 1
    tmp_f.write(str(cmdhist_time) + " " + user + ":" + lsh_hostname + " | " + cmd + "\n")


def load_command_config():
    commands_path = os.path.join(lsh_path_fixed, "config", "commands.json")
    try:
        with open(commands_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            commands = data.get("commands", [])
            if not isinstance(commands, list):
                raise TypeError("commands should be a list")
            return commands
    except FileNotFoundError:
        logger.error("Commands config missing: %s", commands_path)
        return []
    except (json.decoder.JSONDecodeError, TypeError):
        input(f"[JSON Syntax Incorrect] {commands_path} Press any key to except")
        return []


def normalize_command_file_name(command_name):
    return command_name.replace(" ", "_")


def resolve_command_spec(cmd, command_list):
    best = None
    for spec in command_list:
        name = spec.get("name")
        if name == cmd:
            return spec
        if spec.get("accept_args") and name and cmd.startswith(name + " "):
            if best is None or len(name) > len(best.get("name", "")):
                best = spec
    return best


def execute_command_text(spec, cmd):
    file_name = spec.get("file")
    if not file_name:
        file_name = normalize_command_file_name(spec.get("name", "")) + ".txt"
    file_path = os.path.join(lsh_path_fixed, "config", "commands", file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print("命令定义文件缺失: " + file_name)
        return
    globals()["cmd"] = cmd
    try:
        exec(compile(code, file_path, "exec"), globals())
    except Exception as command_error:
        print("执行命令时发生错误: " + str(command_error))


def execute_command(cmd):
    cmd = cmd.rstrip()
    spec = resolve_command_spec(cmd, command_list)
    if not spec:
        if rsyscmd_when_cnf:
            print("未知命令，正在尝试运行命令于主机系统。")
            os.system(cmd)
        else:
            beep()
            visuallog("Unknown command m(__)m : " + cmd, 2)
            print(color.red + "[未知命令]" + color.reset, end=' ')
            logger.error("tty1/lsh | " + cmd + " | Command not found!")
        return
    typ = spec.get("type", "shell")
    if typ == "shell":
        if "cmd" in spec:
            os.system(spec["cmd"])
        else:
            command_text = spec.get("cmd_windows") if isWindows else spec.get("cmd_posix")
            if command_text:
                os.system(command_text)
            else:
                print("命令配置错误: " + str(spec))
    elif typ == "python":
        runPreInstApp(lsh_path_fixed + "/" + spec["target"])
    elif typ == "python_template":
        name = spec.get("name", "")
        rest = cmd[len(name):].lstrip()
        target = spec["target"].format(rest=rest)
        runPreInstApp(lsh_path_fixed + "/" + target)
    elif typ == "text":
        execute_command_text(spec, cmd)
    else:
        print("未知命令类型: " + typ)


command_list = load_command_config()

class AutoexecuteAssignmentLogger(ast.NodeTransformer):
    def _collect_target_names(self, targets):
        names = []
        for target in targets:
            names.extend(self._collect_target_names_from_node(target))
        return names

    def _collect_target_names_from_node(self, node):
        if isinstance(node, ast.Name):
            return [node.id]
        if isinstance(node, (ast.Tuple, ast.List)):
            names = []
            for elt in node.elts:
                names.extend(self._collect_target_names_from_node(elt))
            return names
        return []

    def _make_change_log(self, name):
        return ast.Expr(value=ast.Call(
            func=ast.Name(id="print", ctx=ast.Load()),
            args=[
                ast.Constant(value=f"[autoexecute] variable changed: {name}"),
                ast.Constant(value="->"),
                ast.Name(id=name, ctx=ast.Load()),
            ],
            keywords=[],
        ))

    def visit_Assign(self, node):
        node = self.generic_visit(node)
        statements = [node]
        for name in self._collect_target_names(node.targets):
            statements.append(self._make_change_log(name))
        return statements

    def visit_AugAssign(self, node):
        node = self.generic_visit(node)
        statements = [node]
        for name in self._collect_target_names([node.target]):
            statements.append(self._make_change_log(name))
        return statements

    def visit_AnnAssign(self, node):
        node = self.generic_visit(node)
        statements = [node]
        for name in self._collect_target_names([node.target]):
            statements.append(self._make_change_log(name))
        return statements


def contains_effectful_autoexecute_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return True
    effectful_node_types = (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Delete, ast.Import, ast.ImportFrom)
    for node in ast.walk(tree):
        if isinstance(node, effectful_node_types):
            return True
    return False


def transform_autoexecute_code(code, autoexec_path):
    if not autoexecute_show_variable_changes:
        return compile(code, autoexec_path, "exec")
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return compile(code, autoexec_path, "exec")
    transformed_tree = AutoexecuteAssignmentLogger().visit(tree)
    ast.fix_missing_locations(transformed_tree)
    return compile(transformed_tree, autoexec_path, "exec")


def run_autoexecute_script():
    autoexec_path = os.path.join(lsh_path_fixed, "autoexecute.py")
    if not os.path.isfile(autoexec_path):
        return
    with open(autoexec_path, "r", encoding="utf-8") as autoexec_file:
        code = autoexec_file.read()
    if autoexecute_prompt_on_effects and contains_effectful_autoexecute_code(code):
        try:
            prompt_reply = input("检测到 autoexecute.py 中含有不安全的代码，会修改您的环境变量，确实要执行吗？[Y/n] ").strip().lower()
        except KeyboardInterrupt:
            print("\n已取消执行 autoexecute.py")
            return
        if prompt_reply not in ("", "y", "yes", "true", "t", "1"):
            print("已跳过执行 autoexecute.py")
            return
    try:
        exec(transform_autoexecute_code(code, autoexec_path), globals())
    except Exception as command_error:
        print("在执行 \"autoexecute\" 时发生错误: " + str(command_error))


def runPreInstApp(pathtoapp):
    if isWindows == True:
        if python_exec_path_windows == "":
            try:
                os.system("python " + pathtoapp)
                rpia_404 = False
            except FileNotFoundError:
                rpia_404 = True
        else:
            try:
                os.system(python_exec_path_windows + " " + pathtoapp)
                rpia_404 = False
            except FileNotFoundError:
                rpia_404 = True
    elif isWindows == False:
        try:
            if venvEnable == True: # bugfix!!!!! --minqwq
                if replace_python_command_to_python3 == True:
                    os.system(venvPath + "3 " + pathtoapp)
                elif replace_python_command_to_python3 == False:
                    os.system(venvPath + " " + pathtoapp)
                else:
                    print("Config incorrect at \"replace_python_command_to_python3\"")
                    print("check it on config/config.json\nif you need help please contact minqwq723897@outlook.com")
                    sys.exit()
            else: # too --minqwq
                if replace_python_command_to_python3 == True:
                    os.system("python " + pathtoapp)
                elif replace_python_command_to_python3 == False:
                    os.system("python3 " + pathtoapp)
                else:
                    print("Config incorrect at \"replace_python_command_to_python3\"")
                    print("check it on config/config.json\nif you need help please contact minqwq723897@outlook.com")
                    sys.exit()
            rpia_404 = False
        except FileNotFoundError:
            rpia_404 = True
    else:
        print("Config incorrect at \"isWindows\"")
        print("check it on config/config.json\nif you need help please contact minqwq723897@outlook.com")
        sys.exit()

print(style_cur.hide)
runPreInstApp(lsh_path_fixed + "/apps/coreutils/exampleapp/hello.py")
(1)
clearScreen()
runPreInstApp(lsh_path_fixed + "/coreutil/oeminfo/checkoem.py")
print("VoidFlan Bootstrap")
runPreInstApp(lsh_path_fixed + "/coreutil/bootscr.py")
print(colorama.Fore.LIGHTGREEN_EX + "总内存 " + str(psutil.virtual_memory().total / 1024 / 1024) + " MiB")
print(colorama.Fore.LIGHTGREEN_EX + "初始化完成！")
print("Checking Device UUID Availablity...")
if not os.path.isfile(lsh_path_fixed + "/config/deviceid.txt"):
    print("Not found, Creating one...")
    open(lsh_path_fixed + "/config/deviceid.txt", "w+", encoding="utf-8").write(str(uuid.uuid1()))
    print("ok, now restarting...")
    goto(line=1)
else:
    print("Founded! checking pass.")
time.sleep(1.5)
clearScreen()
print(color.reset)
# Boot manager
bootManagerLoopRun = True
logger.info("Start logging.")
logger.info("Starting VoidFlan Boot manager.")
while bootManagerLoopRun == True:
    print(colorama.Fore.LIGHTRED_EX + "Scarlet Kernel 启动管理器\n" + color.reset + style_cur.show)
    print("\n1:VoidFlan Project " + system_version + "\n9:VoidFlan 应急恢复文档\n2:重启\n3:退出\n4:PY OS Improved Pre-Alpha 1\n5:BBC OS 1.2.1\n8:切到 Leaf Boot Manager（已废弃）")
    if dualBoot == True:
        print(color.green + "\n多启动项已启用。" + color.reset)
        print("6:" + dualBoot_OSName)
    if auto_boot_choice == "":
        print(style.slowblink + "您可以配置 \"auto_boot_choice\" 项为上述选项编号，这样就可以自动选择了。" + color.reset)
        bootChoice = input("> ")
    else:
        bootChoice = auto_boot_choice
    if bootChoice == "1":
        print("...")
        break
    elif bootChoice == "2":
        goto(line=1)
    elif bootChoice == "3":
        sys.exit()
    elif bootChoice == "4":
        clearScreen()
        print("If you want exit, press Ctrl+C to shutdown")
        runPreInstApp(lsh_path_fixed + "/.earlysystem/pyosimproved.py")
        sys.exit()
    elif bootChoice == "5":
        clearScreen()
        print("If you want exit, press Ctrl+C to shutdown")
        runPreInstApp(lsh_path_fixed + "/.earlysystem/bbcos-full.py")
        sys.exit()
    elif bootChoice == "6":
        if dualBoot == True:
            os.system(dualBoot_startupCommand)
            sys.exit()
        elif dualBoot == False:
            pass
    elif bootChoice == "7":
        coresh()
        goto(line=1)
    elif bootChoice == "8":
        visuallog("Not provided in this version", 2)
    elif bootChoice == "9":
        runPreInstApp(lsh_path_fixed + "/coreutil/rescue/issueres.py")
        clearScreen()
        continue
    else:
        visuallog("找不到指定的选项。", 2)
loading_spinner("启动选择项中... ", 1)
clearScreen()
# Startup screen
visuallog("启动主系统中...", 0)
startingtime = time.time()
if faster_startup == True:
    runPreInstApp(lsh_path_fixed + "/coreutil/xubuntustartup_mod.py")
else:
    print("正在启动...")
    if system_is_beta == True: # If is beta version, show this warn
        print(text.doubt + "not release version, may unstable")
    print("[" + color.green + "  OK  " + color.reset + "] Scarlet Kernel 初始化完毕。")
    print("\n" + system_version + "-" + system_codename_lower)
    print("Flandre Studio 2024--2026")
    print("0x1c Studio 2022--2023")
    print("\n" + "* VoidFlan Project 是自由并开放的，您可以随意查看和贡献代码。")
    print("* VoidFlan Project 由 PY OS/BBC OS 1.2.1 改进而来。")
    print("这是个 \"免费软件\"，不会要你钱的。")
    loading_spinner("[" + color.yellow + " WAIT " + color.reset + "] 暂停运行: 3 秒 (按 Ctrl+C 跳过) ", 3)
clearScreen()
end_startingtime = time.time()
startingtime_t = end_startingtime - startingtime
beep()
logger.info("欢迎回到 VoidFlan Project!")
if isWindows == True:
    visuallog("警告: 检测到 Windows 操作系统，目前并未对此做更多优化，不过应该不会影响使用。", 1)
print("VoidFlan Project PhyU/Legacy " + system_version + " \"" + system_codename + "\" " + lsh_hostname) # Login screen | For restart to login manager, please goto this line for work normally
now = datetime.datetime.now()
count = 0
unreg_count = 0
stpasswd = "ciallo"
while count < 3:
    user = input("登录位于 " + lsh_hostname + " 的用户: ")
    if not autologin_username == "":
        user = autologin_username
    if user == "" or user == "defaultuser-000":
        visuallog("登录错误", 2)
    else:
        isCreatorAccount = False
        while count < 3: # 代码难以维护，到处不明变量 --wusheng233
            if logout == True:
                while True:
                    clearScreen()
                    print("系统已被锁定")
                    user = input("登录位于 " + lsh_hostname + " 的用户: ")
                    if user == "":
                        print("未提供字符串")
                    else:
                        break
            if enablePassword == True: # 回上面：那确实，我也不知道啥时候就变成屎山了 --minqwq
                if show_password_when_typing == False:
                    login_password = input("密码: ")
                elif show_password_when_typing == True:
                    try:
                        login_password = getpass.getpass("密码: ")
                    except getpass.GetPassWarning:
                        print("\"show_password_when_typing\": \"false\" - 此配置项可能未按预期工作。")
                if login_password == pwdstring:
                    pass
                else:
                    print("密码错误，请再试一次。")
                    continue
            elif enablePassword == False:
                pass
            else:
                pass
            try:
                clearScreen()
                print("如果您卡在这里了请重新启动。。")
                lshdate = now.strftime("%Y-%m-%d")
                lshtime = now.strftime("%H:%M:%S")
                beep()
                if allowShowNotify == True:
                    try:
                        showNotify("Welcome to VoidFlan Project~!", "Type \"help\" to show all available commands.\nIf you have problem or issue, contact me or open new issue on our official repo.\nhere is my email:minqwq723897@outlook.com")
                    except Exception:
                        if isWindows == False:
                            print("libnotify-bin is not installed, install it from your package manager to enable notify.")
                        elif isWindows == True:
                            print("Unknown error at sending notify")
                elif allowShowNotify == False:
                    pass
                clearScreen()
                if shorter_welcome == False:
                    cat(lsh_path_fixed + "/" + co_welcome) # Welcome text, editable at coreutil/plaintext/welcome.txt
                elif shorter_welcome == True:
                    cat(lsh_path_fixed + "/coreutil/plaintext/welcome_shorter.txt")
                print("今天是 " + colorama.Fore.LIGHTCYAN_EX + lshdate + color.reset + "，时间是 " + colorama.Fore.LIGHTCYAN_EX + lshtime + color.reset)
                welcome_withDetectTime(user)
                if isDev == True:
                    print("dev")
                try:
                    cat(lsh_path_fixed + "/cache/lastlogin.txt")
                except FileNotFoundError:
                    print("上次登录: 未知")
                print("\nFlandre SHell (fsh) version " + colorama.Fore.LIGHTRED_EX + "1.8.0" + color.reset + " >///<\n\"The window of the core...\"")
                tmp_outolog = open("cache/.output.log", "a", encoding="utf-8")
                with open("cache/lastlogin.txt", "w", encoding="utf-8") as ll_wrt:
                    ll_wrt.write("上次登录: " + now.strftime("%b %a %d %H:%M:%S %Y"))
                    print("登录时间更新完毕。")
                try:
                    run_autoexecute_script()
                except Exception as command_error:
                    print("在执行 \"autoexecute\" 时发生错误: " + str(command_error))
                while count < 3:
                    if cmd_theme not in cmd_theme_templates:
                        print("主题没有找到，回到默认。")
                        print("可用主题:default_v2, default, lite, debian_bash, arch_bash, sh, classic, flandre, remilia, tcsh")
                        cmd_theme = "default"
                    cmd_pre = build_cmd_prompt(cmd_theme, user, lsh_hostname, lsh_path)

                    cbatteryperc()
                    if beep_when_finished == True:
                        beep()

                    lsh_time_prepare = datetime.datetime.now()
                    lsh_time = lsh_time_prepare.strftime("%H:%M:%S")
                    if enable_instant_show_time == True:
                        print("[" + lsh_time + "]", end=" ")
                    elif enable_instant_show_time == False:
                        pass
                    # lsh_username = os.system("whoami")
                    cmd = input(cmd_pre)
                    logger.info("[Command] pty0/lsh: " + cmd)
                    # cmdhistory_write()

                    if isUnregistered == True:
                        unreg_count += 1
                        if unreg_count > 25:
                            print("Please register to get best exprience.\nconfig/config.json")
                            unreg_count = 0
                    # Begin commands register

                    pyosi_local_path = os.getcwd()
                    execute_command(cmd) # every command runs here, no error! --Yartmin
            except KeyboardInterrupt: # Ctrl+C, "Ctrl+Alt+Del" like action
                try:
                    print("\n按 1 重启\n其他键取消\n再按一次 Ctrl+C 退出")
                    emergencyChoice = input()
                    if emergencyChoice == "1":
                        goto(line=1)
                except KeyboardInterrupt:
                    clearScreen()
                    sys.exit()
            except FileNotFoundError:
                visuallog("file not found...", 2)
            except Exception as crashReason: # Crash
                time.sleep(0.3) # need this for beep correctly
                beep()
                time.sleep(0.3)
                beep()
                time.sleep(0.3)
                beep()
                clearScreen()
                traceback.print_exception(crashReason, limit=1145, file=sys.stdout) # not working on python 3.8.10
                cat(lsh_path_fixed + "/coreutil/buildtime_styled.txt")
                runPreInstApp("coreutil/catchinfo.py")
                print("Last command input: " + cmd)
                print("Logged on " + user)
                visuallog("System Panic o(╥﹏╥)o : な、何か予期しないエラーが発生しましたにゃ (⁄ ⁄•⁄ω⁄•⁄ ⁄)", 3)
                input("[System Halted, Press any key to shutdown - " + str(crashReason) + "]")
                clearScreen()
                sys.exit()
        if logout == True:
            break
        elif logout == False:
            pass
