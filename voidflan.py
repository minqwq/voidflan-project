# Main code - VoidFlan Project
print("每次重启主机系统后再次启动此程序可能需要一段时间才能初始化，请耐心等待。")
from python_goto import goto
import json
import getpass
import os
import sys
import datetime
import colorama
import time
import random
import platform
import traceback
import logging
import threading
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
import pprint
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
cmdhist_time = "nul"
cmd = "?"
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

# Init configs
try:
    conf = open("./config/config.json", "r", encoding="utf-8")
    devconf = open("./config/.devconfig/confdev.json", "r", encoding="utf-8")
    kiconf = open("./coreutil/module/kernelinfo.json", "r", encoding="utf-8")
    hostconf = open("./config/hostnamecfg.json", "r", encoding="utf-8")
    jsonRead = json.load(conf)
    devJsonRead = json.load(devconf)
    kiJsonRead = json.load(kiconf)
    hostconfJsonRead = json.load(hostconf)
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
    python_exec_path_windows = jsonRead["python_exec_path_windows"] # Python executable path(Windows only, linux/posix use venv instead)
    autologin_username = devJsonRead["autologin_username"]
    enable_legacy_help_engine = jsonRead["enable_legacy_help_engine"]
    expertfeature_cd_enabled = True # cd command availablity
    kernelver = kiJsonRead["version"] # Kernel version
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

def cmdhistory_write():
    tmp_f = open("cache/history.txt", "a", encoding="utf-8")
    # cmdhist_lines += 1
    cmdhist_timed = datetime.datetime.now().strftime("%b %a %d %H:%M:%S %Y")
    tmp_f.write(str(cmdhist_time) + " " + user + ":" + lsh_hostname + " | " + cmd + "\n")

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
    print("不知道如何抉择时，请选择 1。")
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
        # os.execv(sys.executable, ['python'] + sys.argv) # here, its have issue on windows, so its disabled now --minqwq
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
                while count < 3:
                    if cmd_theme == "default":
                        cmd_pre = colorama.Fore.LIGHTBLUE_EX + user + color.grey + ":" + colorama.Fore.LIGHTCYAN_EX + lsh_hostname + colorama.Fore.LIGHTGREEN_EX + " > " + color.reset
                    elif cmd_theme == "flandre":
                        cmd_pre = colorama.Fore.LIGHTYELLOW_EX + user + color.reset + "/" + colorama.Fore.LIGHTRED_EX + lsh_hostname + color.reset + " ( " + colorama.Fore.LIGHTYELLOW_EX + lsh_path + color.reset + " )" + colorama.Fore.LIGHTRED_EX + " > " + color.reset
                    elif cmd_theme == "remilia":
                        cmd_pre = colorama.Fore.LIGHTBLUE_EX + user + color.reset + "\\" + colorama.Fore.LIGHTMAGENTA_EX + lsh_hostname + color.reset + " { " + colorama.Fore.LIGHTBLUE_EX + lsh_path + color.reset + " } " + colorama.Fore.LIGHTMAGENTA_EX + "> " + color.reset
                    elif cmd_theme == "classic":
                        cmd_pre = user + "@" + lsh_hostname + " " + lsh_path + " > "
                    elif cmd_theme == "sh":
                        cmd_pre = "$ "
                    elif cmd_theme == "default_v2":
                        if getpass.getuser() == "root":
                            cmd_pre = "[*root*] " + color.red + user + ":" + lsh_hostname + color.reset + " [ " + lsh_path + " ] " + color.red + "$ " + color.reset
                        else:
                            cmd_pre = color.green + user + ":" + lsh_hostname + color.reset + " [ " + lsh_path + " ] " + color.green + "$ " + color.reset
                    elif cmd_theme == "lite":
                        cmd_pre = colorama.Fore.GREEN + user + colorama.Fore.LIGHTGREEN_EX + " : " + color.reset
                    elif cmd_theme == "debian_bash":
                        cmd_pre = colorama.Fore.LIGHTGREEN_EX + user + "@" + lsh_hostname + color.reset + ":" + colorama.Fore.LIGHTBLUE_EX + "~" + color.reset + "$ "
                    elif cmd_theme == "arch_bash":
                        cmd_pre = "[" + user + "@" + lsh_hostname + " ~ ] $ "
                    elif cmd_theme == "tcsh":
                        cmd_pre = colorama.Fore.CYAN + lsh_hostname + color.reset + ":" + colorama.Fore.LIGHTWHITE_EX + lsh_path + color.reset + "> "
                    # elif cmd_theme == "qos": # will wont use because its not working actually
                    #     cmd_pre = colorama.Back.BLUE + "[VF]" + colorama.Back.WHITE + colorama.Fore.BLACK + " --:--:-- " + colorama.Style.RESET_ALL + colorama.Fore.WHITE + colorama.Back.GREEN + " " + user + " " + colorama.Style.RESET_ALL + " > " + colorama.Fore.LIGHTGREEN_EX + " ~ $ " + colorama.Style.RESET_ALL
                    else:
                        print("主题没有找到，回到默认。")
                        print("可用主题:default_v2, default, lite, debian_bash, arch_bash, sh, classic, flandre, remilia, tcsh")
                        cmd_theme = "default"

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

                    if cmd == "ls": # Path
                        if isWindows == False:
                            os.system("ls ./")
                        elif isWindows == True:
                            os.system("dir .\\")

                    elif cmd == "yukarifm":
                        runPreInstApp(lsh_path_fixed + "/apps/yukarifileman/yukarifm.py")

                    elif cmd == "version":
                        print(system_version + " " + system_codename_lower)

                    elif cmd == "oeminfo":
                        oeminfo.getoeminfo(lsh_path_fixed + "/coreutil/oeminfo/oeminfo.json")
                            
                    elif cmd == "scrtest":
                        runPreInstApp(lsh_path_fixed + "/apps/coreutils/scrtest/scrtest.py")

                    elif cmd == "help":
                        if enable_legacy_help_engine == False:
                            runPreInstApp(lsh_path_fixed + "/apps/coreutils/help/cmdListParser.py")
                        elif enable_legacy_help_engine == True:
                            cat(lsh_path_fixed + "/" + co_manualHelp)

                    elif cmd == "morifetchex":
                        currentUptime = time.time()
                        currentUptimeII = currentUptime - end_startingtime
                        formattedUptime = timeformat(currentUptimeII)
                        mori(user, lsh_hostname, lsh_path, "config/config.json", "config/.devconfig/confdev.json", formattedUptime, deviceid)
                    
                    elif cmd.startswith("kernlog"):
                        try:
                            level = int(cmd[8:9])
                            string = cmd[10:]
                            visuallog(string, level)
                        except Exception:
                            visuallog("格式错误，应为 kernlog <level> <str>", 2)

                    elif cmd.startswith("whereis"):
                        whereisword = cmd[8:]
                        filesearch(whereisword)

                    elif cmd.startswith("pymodpl"):
                        tmp_pymodpl_fname = cmd[8:]
                        try:
                            pymodpl_thread.stop()
                        except Exception:
                            pass
                        pymodpl_thread = threading.Thread(target=pymodpl.play_stdfile(tmp_pymodpl_fname))
                        pymodpl_thread.daemon = True
                        pymodpl_thread.start()

                    elif cmd == "krmidipl":
                        runPreInstApp(lsh_path_fixed + "/apps/krmidipl/runme.py")

                    elif cmd.startswith("cd"):
                        if expertfeature_cd_enabled == True:
                            chdir = cmd[3:]
                            try:
                                os.chdir(chdir)
                                lsh_path = os.getcwd()
                                if disablePathShow == True:
                                    lsh_path = "DISABLED"
                            except FileNotFoundError:
                                print("路径未找到: " + chdir)

                    elif cmd == "netrefresh":
                        if netcheck("main.minqwq.moe", 80):
                            networked = True
                            print("[" + color.green + "  OK  " + color.reset + "] Network return True, enabled")
                        else:
                            print("[" + color.red + " FAIL " + color.reset + "] Network return False, if you have tryed to reconnect, retry run \"netrefresh\"")
                    elif cmd.startswith("netrefresh set"):
                        if cmd[15:] == True or cmd[15:] == True:
                            networked = True
                            print("networked = " + str(networked))
                        elif cmd[15:] == False or cmd[15:] == False:
                            networked = False
                            print("networked = " + str(networked))
                        else:
                            print("True, true, False, false")
                    elif cmd == "netrefresh -h":
                        cat(lsh_path_fixed + "/coreutil/plaintext/netrefresh_help.txt")
                        print(system_version)

                    elif cmd == "jrrp":
                        print("今日人品 " + str(random.randint(0, 100)))

                    elif cmd == "logout":
                        print("登出...")
                        logout = True
                        break

                    elif cmd == "pyosiupgrade":
                        print("更新系统中...(Development Channel)")
                        os.system("git pull --no-rebase")
                        print("请关闭此程序再打开以应用更新。")

                    elif cmd == "weather":
                        runPreInstApp(lsh_path_fixed + "/apps/weather/weather-api.py")

                    elif cmd.startswith("stdoutredirect"):
                        if cmd[16:] == "":
                            print("未键入字符串。")
                        else:
                            sys.stdout = cmd[16:]

                    elif cmd == "ed":
                        runPreInstApp(lsh_path_fixed + "/apps/ed-editor/edit.py")

                    # Package manager info
                    elif cmd == "shizuku":
                        szkmng.tips()
                    elif cmd == "shizuku list":
                        szkmng.list_apps()
                    elif cmd.startswith("shizuku run"):
                        os.chdir(lsh_path_fixed + "/extprog")
                        runPreInstApp(cmd[11:] + ".py")
                        os.chdir("../")
                    # Package install
                    elif cmd.startswith("shizuku install"):
                        pkgPath = cmd[16:]
                        print("正在安装来自 " + pkgPath + " 的软件包...")
                        result = szkmng.install(pkgPath)
                        os.chdir(pyosi_local_path)
                        if result != 0:
                            print("安装失败。")
                    # Package remove
                    elif cmd.startswith("shizuku remove"):
                        rm_app_name = cmd[15:]
                        print("开始卸载软件包: " + rm_app_name + " ...")
                        result = szkmng.remove(rm_app_name)
                        os.chdir(pyosi_local_path)
                        if result != 0:
                            print("卸载失败")
                    # The credits
                    elif cmd.startswith("shizuku credits"):
                        cat(lsh_path_fixed + "/coreutil/plaintext/shizuku_credits.txt")

                    elif cmd.startswith("chthm"):
                        cmd_theme = cmd[6:]
                        logger.info("Shell theme changed to " + cmd[6:])
                        print("Shell 主题已设置为 " + cmd[6:])

                    elif cmd == "patch":
                        pprint.pprint(dict(globals()))
                    elif cmd == "patch --set":
                        confsel1 = input("set <confsel1> = <confsel2>(cur:sel1): ")
                        confsel2 = input("set <confsel1> = <confsel2>(cur:sel2): ")
                        os.environ[confsel1] = confsel2

                    elif cmd == "asciicvt":
                        runPreInstApp(lsh_path_fixed + "/apps/asciicvt/asciiconverter.py")

                    elif cmd == "tasks":
                        os.system("cd ./home/public/savedfile/tasks && ../../apps/tasks/tasks && cd ../..")

                    elif cmd == "2048":
                        os.system(lsh_path_fixed + "/apps/2048/2048-in-terminal")

                    elif cmd.startswith("su"):
                        user_preInput = cmd[3:]
                        if user_preInput == "":
                            print("未指定用户。")
                        else:
                            user = user_preInput
                            print("切换用户到 " + user)
                            logger.info("[Login manager] Switch user to " + user)

                    elif cmd == "rss":
                        runPreInstApp(lsh_path_fixed + "/apps/rss/main.py")

                    elif cmd == "crash":
                        if user == "dev":
                            logger.warn("Congrats, you make the VoidFlan Project crashed.")
                            raise EOFError("by urself")
                        else:
                            os.chdir(lsh_path_fixed + "/apps")
                            cat_bugged("coreutil/plaintext/manualhelp.txt")

                    elif cmd.startswith("echo "):
                        string = cmd[5:]
                        if string == "":
                            print("未提供字符串")
                        else:
                            print(string)

                    elif cmd == "clock":
                        runPreInstApp(lsh_path_fixed + "/apps/clock/clock.py")

                    elif cmd == "ttt":
                        runPreInstApp(lsh_path_fixed + "/apps/tictactoe/tictactoe.py")

                    elif cmd == "paint":
                        paintWidthAndHeight = input("Input width and height(example:50 50): ")
                        os.chdir(lsh_path_fixed + "/home/public/savedfile")
                        runPreInstApp("../apps/paint/paint.py " + paintWidthAndHeight)
                        os.chdir("..")

                    elif cmd == "pftest":
                        runPreInstApp(lsh_path_fixed + "/apps/pftest/mark.py")

                    elif cmd == "demine":
                        os.system(lsh_path_fixed + "/apps/minesweeper/minesweeper")

                    elif cmd == "fileget":
                        os.chdir(lsh_path_fixed + "/download")
                        runPreInstApp("../apps/fileget/fileget.py")
                        os.chdir("..")

                    elif cmd == "uptime":
                        currentUptime = time.time()
                        print(currentUptime - end_startingtime)

                    elif cmd == "guessnum":
                        runPreInstApp(lsh_path_fixed + "/apps/guessnum/guessnum.py")

                    elif cmd == "hostname":
                        print(lsh_hostname)
                    elif cmd == "hostname -c":
                        lsh_hostname_pre = input("> ")
                        if lsh_hostname_pre == "":
                            print("未提供字符串")
                        else:
                            lsh_hostname = lsh_hostname_pre

                    elif cmd.startswith("szk"):
                        # 提取包名，即命令去掉前四个字符后的部分
                        pypkg = cmd[4:]
                        if isWindows == True:
                            try:
                                os.chdir(".\\data\\apps\\" + pypkg)
                                runPreInstApp(pypkg + ".py")
                            except FileNotFoundError:
                                print("未找到程序包: " + pypkg)
                                os.chdir(pyosi_local_path)
                            except Exception as e:
                                print("错误: " + str(e))
                                os.chdir(pyosi_local_path)
                            finally:
                                os.chdir(pyosi_local_path)
                        elif isWindows == False:
                            try:
                                os.chdir(lsh_path_fixed + "/data/apps/" + pypkg)
                                print("EXECUTABLE=" + sys.executable)
                                runPreInstApp(pypkg + ".py")
                            except FileNotFoundError:
                                print("未找到程序包: " + pypkg)
                                os.chdir(pyosi_local_path)
                            except Exception as e:
                                print("错误: " + str(e))
                                os.chdir(pyosi_local_path)
                            finally:
                                os.chdir(pyosi_local_path)

                    elif cmd == "about": # About system
                        slowprint("---------------| 关于 |---------------")
                        print(color.blue + "VoidFlan Project " + system_version + "-" + system_codename_lower + " \"" + system_codename + "\" by Yartmin Scarlet" + color.reset)
                        print("(C) " + color.green + "0x1c Studio " + color.reset + "2022--2023 | (C) " + colorama.Fore.LIGHTRED_EX + "Flandre" + color.red + " Studio 芙兰社 " + color.reset + "2022--2025" + color.reset)
                        print("Python 环境版本: " + str(platform.python_version()))
                        if isDevchan == True:
                            print("位于测试频道")
                        print(" ")
                        print("-l 查看协议")
                    elif cmd == "about -l":
                        cat(lsh_path_fixed + "/LICENSE")

                    elif cmd == "power":
                        print("请指定一个选项。")
                    elif cmd == "power shutdown" or cmd == "st" or cmd == ":q" or cmd == "halt": # Shutdown
                        logger.info("Shutting down...")
                        sys.exit()
                    elif cmd == "power reboot" or cmd == "reboot":
                        visuallog("电符 [世界重启]", 0)
                        clearScreen()
                        os.execl(sys.executable, sys.executable, *sys.argv)

                    elif cmd == "time": # Show current time
                        now = datetime.datetime.now()
                        other_StyleTime = now.strftime("%b %a %d %H:%M:%S %Y")
                        print(other_StyleTime)
                        
                    elif cmd == "caesar":
                        os.chdir(lsh_path_fixed + "/apps/caesartools")
                        runPreInstApp("caesar.py")
                        os.chdir("../..")

                    elif cmd == "cuscmd":
                        print("现在开始输入要运行的命令。")
                        customCommand = input("")
                        os.system(customCommand)

                    elif cmd == "":
                        space = 0

                    elif cmd == "clear":
                        clearScreen()

                    elif cmd == "exit":
                        clearScreen()
                        systemIsLocked = True
                        print("VoidFlan " + system_version + " 已锁定")
                        print("按u解锁，输time查看时间，输st关机")
                        while systemIsLocked == True:
                            unlockSystem = input("")
                            if unlockSystem == "u":
                                systemIsLocked = False
                                clearScreen()
                                break
                            elif unlockSystem == "time":
                                now = datetime.datetime.now()
                                other_StyleTime = now.strftime("%b %a %d %H:%M:%S %Y")
                                print(other_StyleTime)
                            elif unlockSystem == "st":
                                clearScreen()
                                sys.exit()
                    else: # Wrong command
                        if rsyscmd_when_cnf == True:
                            print("未知命令，正在尝试运行命令于主机系统。")
                            os.system(cmd)
                        elif rsyscmd_when_cnf == False:
                            beep()
                            visuallog("Unknown command m(__)m : " + cmd, 2)
                            print(color.red + "[未知命令]" + color.reset, end=' ')
                            logger.error("tty1/lsh | " + cmd + " | Command not found!")
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
                traceback.print_exception(crashReason, limit=1145, file=sys.stdout)
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
