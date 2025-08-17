# Main code - VoidFlan Project
print("First running may take long time in some device, if this happen please just wait.(if its not responding at somewhere please press Ctrl+C and restart.)")
from python_goto import goto # Goto a line
import json # Read json file(config file need this)
conf = open("./config/config.json", "r", encoding="utf-8")
devconf = open("./config/.devconfig/confdev.json", "r", encoding="utf-8")
jsonRead = json.load(conf)
devJsonRead = json.load(devconf)
# jsonWrite = open("config/config.json", "w", encoding="utf-8")
import time as tm # Time
import getpass # Password?
import calendar # Calendar
import os # Communicate to your system
import sys # idk
import datetime
import colorama
import time # Time
import random # Random tools
from os import path # Path control
sys.path.append("./")
import platform
import requests # Get file from server
import base64 # Encode and decode
import traceback
import logging # Log.
import profile # used only at startup screen and you can remove it
import subprocess
import re
import autoexec
import threading
import uuid
# import coreutil.moddedprogram.pymodpl as pymodpl
try:
    from coreutil.module.actions import *
    from coreutil.module.style import *
    from coreutil.module.textmoji import *
    from coreutil.module.splashes import *
    from coreutil.module.network import *
except Exception:
    visuallog("Kernel Panic!!", 3)
    sys.exit(15)
visuallog("Kernel is ready.", 0)
try:
    import curses
except ModuleNotFoundError:
    print("If you are trying run this on windows, please install curses module.")
    sys.exit(1)
try:
    import pygame
    haveSoundCard = True
except Exception:
    print("pygame not found or error, some program may not work.")
    haveSoundCard = False
import art
import pprint
import coreutil.shizuku.manager as szkmng # Installer for shizuku
import coreutil.oeminfo.printoeminfo as oeminfo
# import core.module.history as history
print("\033[?25l")
class override:
    errorexpection = "teto:ErrorExpection"
    tongue = "teto:a-------"
def echo(string):
    print(string)
# pretty_errors.configure(
#    postfix               = '!!! FALLBACK CRASH SCREEN !!!\nPY OS Improved has been crashed.\nRestart command:python pyosimproved.py\nReport this error!:https://github.com/minqwq/pyos-improved/issues',
#    separator_character   = '#',
#    line_color            = colorama.Fore.LIGHTBLUE_EX + 'Here > ' + color.reset,
# print("config updated for pretty-errors")

# i love bai9nine and minimalmio --minqwq 2025-02-19
# and my best friend stevemcpe
# 19740914

cmdhist_lines = 0
cmdhist_time = "nul"
lsh_hostname = "scarletlocal-000"
user = "defaultuser_nologin"
lsh_path = os.getcwd()
lsh_path_fixed = os.getcwd()
networked = False
rpia_404 = False
debugMode = ""

LOG_FORMAT = '[Embedded][%(levelname)s] %(asctime)s | %(message)s'
logging.basicConfig(filename='cache/.output.log', datefmt='%b %a %d %H:%M:%S %Y', level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.info("Logger started successfully.")

# CONFIG START
system_version = devJsonRead["system_version"] # 版本号 / Version
system_codename = devJsonRead["system_codename"] # Codename
system_build = devJsonRead["system_build"] # 每做一个修改或增减内容，就加一个 Build / If changed a feature, build +=1
system_is_beta = False # 是否为 Beta 版 / Beta version
isWindows = jsonRead["isWindows"] # 是否为 Windows / Are you windows?
cmd_theme = jsonRead["cmd_theme"] # 终端 Shell 主题 / Terminal shell theme
isDev = False # 是否为 Dev 模式 / Dev mode
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
if venvEnable == "true":
    venvPath = jsonRead["venvPath"] # If you are linux distro, like me, you need this
replace_python_command_to_python3 = jsonRead["replace_python_command_to_python3"] # Replace python command to python3(when you using linux distro)
disablePathShow = jsonRead["disablePathShow"] # Disable path show on shell
shorter_welcome = jsonRead["shorter_welcome"] # Show shorter welcome text when logon
faster_startup = jsonRead["faster_startup"] # New version of startup screen
rsyscmd_when_cnf = jsonRead["rsyscmd_when_cnf"] # Run system command when command not found
lsh_hostname = jsonRead["default_hostname"] # Your default hostname(Boot ID 1 only)
autologin_username = devJsonRead["autologin_username"]
enable_legacy_help_engine = jsonRead["enable_legacy_help_engine"]
try:
    deviceid = open(lsh_path_fixed + "/config/deviceid.txt", "r", encoding="utf-8").readline().strip()
except Exception:
    pass
# EXPERTIONAL FEATURE

readConfigFromExport = False # Linux only! windows have same but not a command.
disableKernelFeature = False # Disable the kernel, may crash more.
expertfeature_cd_enabled = True # cd command availablity

# EXPERTIONAL FEATURE
# DYNAMIC CONFIG
logout = False
# DYNAMIC CONFIG END
# CONFIG END

if disablePathShow == "true":
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
    if isWindows == "true":
        try:
            os.system("python " + pathtoapp)
            rpia_404 = False
        except FileNotFoundError:
            rpia_404 = True
    elif isWindows == "false":
        try:
            if venvEnable == "true": # bugfix!!!!! --minqwq
                if replace_python_command_to_python3 == "true":
                    os.system(venvPath + "3 " + pathtoapp)
                elif replace_python_command_to_python3 == "false":
                    os.system(venvPath + " " + pathtoapp)
                else:
                    print("Config incorrect at \"replace_python_command_to_python3\"")
                    print("check it on config/config.json\nif you need help please contact minqwq723897@outlook.com")
                    sys.exit()
            else: # too --minqwq
                if replace_python_command_to_python3 == "true":
                    os.system("python " + pathtoapp)
                elif replace_python_command_to_python3 == "false":
                    os.system("python3 " + pathtoapp)
                else:
                    print("Config incorrect at \"replace_python_command_to_python3\"")
                    print("check it on config/config.json\nif you need help please contact minqwq723897@outlook.com")
                    sys.exit()
            rpia_404 = False
        except FileNotFoundError:
            rpia_404 = True

def termux_detect():
    return "TERMUX_VERSION" in os.environ

# with open("./config/config.json", "w", encoding="utf-8") as temp_writeConfig:
#
"""
def compWizard():
    print("Comptiable Wizard\ntrue if you are windows\nfalse if you are *nix")
    conf_isWindows_write = input("> ")
    if conf_isWindows_write == "false":
        jsonRead["isWindows"] = "false"
        json.dump(jsonRead, jsonWrite, indent=4)
        print("You can restart now.")
    elif conf_isWindows_write == "true":
        jsonRead["isWindows"] = "true"
        json.dump(jsonRead, jsonWrite, indent=4)
        print("You can restart now.")
    # print("Please configure the 'isWindows' to false or true on config/config.json\nIt's looks like this:\"isWindows\": \"\", Change it to:\n\"isWindows\": \"false\" If you are linux\n\"isWindows\": \"true\" If you are windows")
    # print("Exiting...")
    # sys.exit()
    else:
        print("Please retry.")
"""

def clearScreen():
    print("\033[2J" + "\033[0;0H")

def beep():
    print("\a", end="\r")

loadtime_aftered = 0
temp_clock1 = time.time()

if temp_clock1 < 2:
    goto(line=181)

print("Other utils loaded")
print(style_cur.hide)
import psutil
clearScreen()
visuallog("in the shortly future, we will change the project name to VoidFlan or DarkReedy", 1)
print(colorama.Fore.LIGHTGREEN_EX + "Native + Extended Memory Total " + str(psutil.virtual_memory().total / 1024) + " KBytes(i)")
print(colorama.Fore.LIGHTGREEN_EX + "System Kernel init successful!")
print("Checking Device UUID Availablity...")
if not os.path.isfile(lsh_path_fixed + "/config/deviceid.txt"):
    print("Not found, Creating one...")
    open(lsh_path_fixed + "/config/deviceid.txt", "w+", encoding="utf-8").write(str(uuid.uuid1()))
    print("Restarting...")
    goto(line=1)
else:
    print("Founded! checking pass.")
time.sleep(1.5)
clearScreen()
print(color.reset)
time.sleep(0.1)
# Boot manager
bootManagerLoopRun = True
logger.info("Start logging.")
logger.info("Starting VoidFlan Boot manager.")
while bootManagerLoopRun == True:
    print(colorama.Fore.LIGHTRED_EX + "Scarlet Kernel Boot manager\n" + colorama.Fore.LIGHTYELLOW_EX + "  -- version II series" + color.reset + style_cur.show)
    print("If you dont know which to choose, choose 1 and then continue.")
    print("\n1:VoidFlan Project " + system_version + "\n9:VoidFlan Rescue Mode\n2:Reboot\n3:Shutdown\n4:PY OS Improved Pre-Alpha 1\n5:BBC OS 1.2.1\n8:Switch to Leaf Boot manager(new!)")
    if dualBoot == "true":
        print(color.green + "\nDUAL BOOT ENABLED" + color.reset)
        print("6:" + dualBoot_OSName)
    if auto_boot_choice == "":
        print(style.slowblink + "You can set \"auto_boot_choice\" to a number to set auto select!" + color.reset)
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
        if dualBoot == "true":
            os.system(dualBoot_startupCommand)
            sys.exit()
        elif dualBoot == "false":
            pass
    elif bootChoice == "7":
        coresh()
    elif bootChoice == "8":
        visuallog("Not provided in this version", 2)
    elif bootChoice == "9":
        runPreInstApp(lsh_path_fixed + "/coreutil/rescue/issueres.py")
        clearScreen()
        continue
    else:
        visuallog("Operating System not found - Bad Boot ID", 2)
loading_spinner("Booting... ", 1)
clearScreen()
# Startup screen
visuallog("Starting main operating system...", 0)
startingtime = time.time()
if faster_startup == "true":
    runPreInstApp(lsh_path_fixed + "/coreutil/xubuntustartup_mod.py")
else:
    print("Starting up...")
    if system_is_beta == True: # If is beta version, show this warn
        print(text.doubt + "not release version, may unstable")
    print("[" + color.yellow + " LOAD " + color.reset + "] Initialing Scarlet Kernel...")
    time.sleep(0.1)
    sk_act_about()
    sk_stl_about()
    sk_tm_about()
    sk_net_about()
    time.sleep(0.1)
    print("[" + color.green + "  OK  " + color.reset + "] Scarlet Kernel initialion complete")
    """
    print("[" + color.yellow + " WAIT " + color.reset + "] Initialing network... checking... connecting to main.minqwq.moe:80 ...(Press Ctrl+C to skip)")
    try:
        if netcheck("main.minqwq.moe", 80):
            networked = True
            print("[" + color.green + "  OK  " + color.reset + "] Network return True, enabled")
        else:
            print("[" + color.red + " FAIL " + color.reset + "] Network return False, if you have tryed to reconnect, login and run \"netrefresh\"")
    except KeyboardInterrupt:
        networked = False
        print("[" + color.yellow + " WARN " + color.reset + "] Skipped network checking, will keep status \"False\".")
    """
    print("\n" + system_version + " " + system_build)
    print("Flandre Studio 2024--2025")
    print("0x1c Studio 2022--2023")
    print("\n" + "* VoidFlan Project is a Open-Source fake operating system, so fell free to improve our code!")
    print("* VoidFlan Project is inspired from PY OS/BBC OS 1.2.1 not 2.0 or later.")
    print("This is a \"freeware\".")
    loading_spinner("[" + color.yellow + " WAIT " + color.reset + "] Delay: 3 secs (Press Ctrl+C to skip) ", 3)
clearScreen()
time.sleep(0.1)
"""
aprilFoolsTimeCheck = time.time()
print(str(aprilFoolsTimeCheck))
if aprilFoolsTimeCheck < 1743523200:
    print(text.error + color.red + "Your system has been hacked by minqwq!!!!!!\nPlease type the coorrect password to unlock.")
    getAFUnlock = input("type decoded of this string(after you decoded, if you see 0 and 1 please decode again)\nMTEwMTExMCAxMTAwMDAxIDExMDExMTAgMTEwMDAwMSAxMTAxMTAxIDExMDEwMDE=\n>")
    if getAFUnlock == "nanami":
        pass
    else:
        while True:
            print(text.error + color.red + "Your system is being to destroy...")
            time.sleep(0.1)
"""
end_startingtime = time.time()
startingtime_t = end_startingtime - startingtime
beep()
logger.info("Welcome to VoidFlan Project!")
if isWindows == "true":
    visuallog("Operating System Incomptiable warning: Some program may not working on your PC.", 1)
print("Welcome to VoidFlan Project \"Flandre/Scarlet Kernel I\" PYOS/Legacy version " + system_version + " " + lsh_hostname) # Login screen | For restart to login manager, please goto this line for work normally
print("\n" + random.choice(splashes))
now = datetime.datetime.now()
# other_StyleTime = now.strftime("%b %a %d %H:%M:%S %Y")
count = 0
unreg_count = 0
stpasswd = "ciallo"
while count < 3:
    if not autologin_username == "":
        user = autologin_username
    elif debugMode == "":
        user = input(lsh_hostname + " login " + color.blue + "--> " + color.reset)
    if user == "gaster":
        goto(line=0)
    elif user == "":
        time.sleep(1.5)
        print("Login incorrect")
    elif user == "bai9nine":
        print("nope.   --minqwq")
    elif user == "yukari2024":
        print(colorama.Back.LIGHTBLUE_EX + "VoidFlan Project has been terminated.")
        print("and this is not a issue, its just a easter egg." + color.reset)
        sys.exit()
    elif user == "yukari":
        print(colorama.Back.LIGHTBLUE_EX + "nope bro")
        print("change her's second name and retry to login is useless." + color.reset)
        sys.exit()
    elif user == "koishi":
        for idk in range(100000):
            print(colorama.Fore.LIGHTRED_EX)
            print("die", end="")
        for idk2 in range(50000):
            print("look back ", end="")
        for idk3 in range(20):
            for idk4 in tqdm.tqdm(range(5114)):
                print(colorama.Fore.LIGHTRED_EX + "die!!!", end="")
            d.infobox("N? Si??a?", width=0, height=0, title="Er??r")
            time.sleep(random.random())
            clearScreen()
        time.sleep(0.1)
        clearScreen()
        print("You have been kicked by Komeiji Koishi.\nPlease r???\nP??\nPlease re-lo??..gin.")
    elif user == "mibino":
        print("nope")
        sys.exit()
    else: # a lot of shit code here --minqwq
        isCreatorAccount = False
        while count < 3: # 代码难以维护，到处不明变量 --wusheng233
            if enablePassword == "true": # 回上面：那确实，我也不知道啥时候就变成屎山了 --minqwq
                if show_password_when_typing == "false":
                    login_password = input("Password: ")
                elif show_password_when_typing == "true":
                    try:
                        login_password = getpass.getpass("Password: ")
                    except getpass.GetPassWarning:
                        print("\"show_password_when_typing\": \"false\" is not working.")
                if login_password == pwdstring:
                    pass
                else:
                    print("Incorrect password, please re-enter")
                    continue
            elif enablePassword == "false":
                pass
            else:
                pass
            try:
                clearScreen()
                print("If you are stucked on this screen please press Ctrl+C and then restart")
                lshdate = now.strftime("%Y-%m-%d")
                lshtime = now.strftime("%H:%M:%S")
                if user == "minqwq":
                    # password_pre = b"aWxvdmVtaW8="
                    # password = base64.b64decode(password_pre)
                    # inputpass = bytes(input(), encoding="utf-8")
                    creatorVerifyPassword = base64.b64decode(b"cXdlMTE1MDYx")
                    creatorVerify = bytes(getpass.getpass("Verify required, please type password...\n> "), encoding="utf-8")
                    if creatorVerify == creatorVerifyPassword:
                        clearScreen()
                        print("The creator of VoidFlan Project, welcome back.\n")
                        isCreatorAccount = True
                    else:
                        print(color.red + "Access Denied." + color.reset)
                        sys.exit()
                elif user == "dev":
                    clearScreen()
                    print("You are trying to login dev account, please input the password below:")
                    deVerify = input("")
                    if deVerify == "ilovemio":
                        isDev = True
                    else:
                        clearScreen()
                        sys.exit()
                beep()
                if allowShowNotify == "true":
                    try:
                        showNotify("Welcome to VoidFlan Project~!", "Type \"help\" to show all available commands.\nIf you have problem or issue, contact me or open new issue on our official repo.\nhere is my email:minqwq723897@outlook.com")
                    except Exception:
                        if isWindows == "false":
                            print("libnotify-bin is not installed, install it from your package manager to enable notify.")
                        elif isWindows == "true":
                            print("Unknown error at sending notify")
                elif allowShowNotify == "false":
                    pass
                clearScreen()
                if shorter_welcome == "false":
                    cat(lsh_path_fixed + "/" + co_welcome) # Welcome text, editable at coreutil/plaintext/welcome.txt
                elif shorter_welcome == "true":
                    cat(lsh_path_fixed + "/coreutil/plaintext/welcome_shorter.txt")
                print("\nH-hi thewe " + color.cyan + user + color.reset + " >///<, I-I missed you a-a lot.")
                print("Today is " + colorama.Fore.LIGHTCYAN_EX + lshdate + color.reset + " and time is " + colorama.Fore.LIGHTCYAN_EX + lshtime + color.reset + ".\nWeather is not bad.\n")
                welcome_withDetectTime(user)
                autoexec.main()
                # print(style.slowblink + "Happy china lunar year(2025-01-28)!" + color.reset)
                if isDev == True:
                    print("Logged into dev account, some command may unlocked!")
                try:
                    cat(lsh_path_fixed + "/cache/lastlogin.txt")
                except FileNotFoundError:
                    print("Last login: Unknown, did you just deleted this file or first using?")
                print("\nFlandre SHell (fsh) version " + colorama.Fore.LIGHTRED_EX + "1.8.0" + color.reset + " >///<\n\"The window of the core...\"")
                tmp_outolog = open("cache/.output.log", "a", encoding="utf-8")
                with open("cache/lastlogin.txt", "w", encoding="utf-8") as ll_wrt:
                    ll_wrt.write("Last login: " + now.strftime("%b %a %d %H:%M:%S %Y"))
                    print("lastlogin written completed.")
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
                    elif cmd_theme == "qos":
                        cmd_pre = colorama.Back.BLUE + "[VF]" + colorama.Back.WHITE + colorama.Fore.BLACK + " --:--:-- " + colorama.Style.RESET_ALL + colorama.Fore.WHITE + colorama.Back.GREEN + " " + user + " " + colorama.Style.RESET_ALL + " > " + colorama.Fore.LIGHTGREEN_EX + " ~ $ " + colorama.Style.RESET_ALL
                    else:
                        print("Theme not found! will do nothing.")
                        print("Available theme name:default_v2, default, lite, debian_bash, arch_bash, sh, classic, flandre")
                        cmd_theme = "default"

                    cbatteryperc()
                    if beep_when_finished == "true":
                        beep()

                    lsh_time_prepare = datetime.datetime.now()
                    lsh_time = lsh_time_prepare.strftime("%H:%M:%S")
                    if enable_instant_show_time == "true":
                        print("[" + lsh_time + "]", end=" ")
                    elif enable_instant_show_time == "false":
                        pass
                    # lsh_username = os.system("whoami")
                    cmd = input(cmd_pre)
                    logger.info("[Command] tty1/lsh: " + cmd)
                    # cmdhistory_write()

                    if isUnregistered == "true":
                        unreg_count += 1
                        if unreg_count > 25:
                            print("Please register to get best exprience.\nconfig/config.json")
                            unreg_count = 0
                    # Begin commands register

                    # pyosi_local_path = os.getcwd() --comment this for disabled, i dont need this one\n if i break somethiing, please uncomment --minqwq

                    if cmd == "ls": # Path
                        if isWindows == "false":
                            os.system("ls ./")
                        elif isWindows == "true":
                            os.system("dir .\\")

                    elif cmd == "oeminfo":
                        oeminfo.getoeminfo(lsh_path_fixed + "/coreutil/oeminfo/oeminfo.json")
                            
                    elif cmd == "scrtest":
                        runPreInstApp(lsh_path_fixed + "/apps/coreutils/scrtest/scrtest.py")

                    elif cmd == "help":
                        if enable_legacy_help_engine == "false":
                            runPreInstApp(lsh_path_fixed + "/apps/coreutils/help/cmdListParser.py")
                        elif enable_legacy_help_engine == "true":
                            cat(lsh_path_fixed + "/" + co_manualHelp)

                    elif cmd == "morifetchex":
                        currentUptime = time.time()
                        currentUptimeII = currentUptime - end_startingtime
                        mori(user, lsh_hostname, lsh_path, "config/config.json", "config/.devconfig/confdev.json", str(round(int(currentUptimeII))), deviceid)
                    
                    elif cmd.startswith("kernlog"):
                        try:
                            level = int(cmd[8:9])
                            string = cmd[10:]
                            visuallog(string, level)
                        except Exception:
                            visuallog("Syntax incorrect.", 2)

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

                    elif cmd == "flashscr":
                        clearScreen()
                        for temp_flashscreen in range(1000):
                            print(colorama.Back.LIGHTWHITE_EX)
                            time.sleep(0.005)
                            print(color.reset)
                            time.sleep(0.005)
                        clearScreen()
                        print("is your eyes still right? or...are you still wake up?")

                    elif cmd.startswith("cd"):
                        if expertfeature_cd_enabled == True:
                            chdir = cmd[3:]
                            try:
                                os.chdir(chdir)
                                lsh_path = os.getcwd()
                                if disablePathShow == "true":
                                    lsh_path = "DISABLED"
                            except FileNotFoundError:
                                print("dir not found: " + chdir)

                    elif cmd == "netrefresh":
                        if netcheck("main.minqwq.moe", 80):
                            networked = True
                            print("[" + color.green + "  OK  " + color.reset + "] Network return True, enabled")
                        else:
                            print("[" + color.red + " FAIL " + color.reset + "] Network return False, if you have tryed to reconnect, retry run \"netrefresh\"")
                    elif cmd.startswith("netrefresh set"):
                        if cmd[15:] == "True" or cmd[15:] == "true":
                            networked = True
                            print("networked = " + str(networked))
                        elif cmd[15:] == "False" or cmd[15:] == "false":
                            networked = False
                            print("networked = " + str(networked))
                        else:
                            print("True, true, False, false")
                    elif cmd == "netrefresh -h":
                        cat(lsh_path_fixed + "/coreutil/plaintext/netrefresh_help.txt")

                    elif cmd == "pyosver":
                        print(system_version + " " + system_build)

                    elif cmd == "jrrp":
                        print("As today, your luck is " + str(random.randint(0, 100)))

                    elif cmd == "logout":
                        print("Return to login manager...")
                        logout = True
                        break

                    elif cmd == "pyosiupgrade":
                        print("Checking and upgrade system...")
                        os.system("git pull --no-rebase")
                        print("Upgrade success, hard restart(shutdown and start again) to take effect.")

                    elif cmd == "weather":
                        runPreInstApp(lsh_path_fixed + "/apps/weather/weather-api.py")

                    elif cmd.startswith("stdoutredirect"):
                        if cmd[16:] == "":
                            print("No string provided.")
                        else:
                            sys.stdout = cmd[16:]

                    elif cmd == "ed":
                        runPreInstApp(lsh_path_fixed + "/apps/ed-editor/edit.py")

                    # Package manager info
                    elif cmd == "shizuku":
                        cat(lsh_path_fixed + "/coreutil/plaintext/extprog_info.txt")
                    elif cmd.startswith("shizuku run"):
                        os.chdir(lsh_path_fixed + "/extprog")
                        runPreInstApp(cmd[11:] + ".py")
                        os.chdir("../")
                    # Package install
                    elif cmd.startswith("shizuku install"):
                        pkgPath = cmd[16:]
                        print("Installing package from " + pkgPath + " ...")
                        if isWindows == "true":
                            # os.system("copy " + pkgPath + " .\\data\\apps")
                            result = szkmng.install(pkgPath)
                            os.chdir(pyosi_local_path)
                            if result != 0:
                                print("Installation failed.")
                        elif isWindows == "false":
                            # os.system("cp " + pkgPath + " ./data/apps")
                            result = szkmng.install(pkgPath)
                            os.chdir(pyosi_local_path)
                            if result != 0:
                                print("Installation failed.")
                    # Package remove
                    elif cmd.startswith("shizuku remove"):
                        rm_app_name = cmd[15:]
                        print("Removing application: " + rm_app_name + " ...")
                        if isWindows == "true":
                            result = szkmng.remove(rm_app_name)
                            os.chdir(pyosi_local_path)
                            if result != 0:
                                print("Removal failed.")
                        elif isWindows == "false":
                            result = szkmng.remove(rm_app_name)
                            os.chdir(pyosi_local_path)
                            if result != 0:
                                print("Removal failed.")
                    # The credits
                    elif cmd.startswith("shizuku credits"):
                        cat(lsh_path_fixed + "/coreutil/plaintext/shizuku_credits.txt")
                    # Package search
                    elif cmd.startswith("shizuku search"):
                        request = cmd[15:]
                        print("This feature is deprecated, please do manually download and install package.")
                    elif cmd.startswith("shizuku flandre"):
                        if cmd[16:] == "_scarlet" or cmd[16:] == " scarlet":
                            print("tomato and fried egg")
                        else:
                            print("you just take her's wings...??")
                    elif cmd == "shizuku scarlet":
                        print("her's wings is not a christmas lights!")

                    elif cmd.startswith("chthm"):
                        cmd_theme = cmd[6:]
                        logger.info("Shell theme changed to " + cmd[6:])
                        print("Successfully seted shell theme " + cmd[6:])

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

                    elif cmd.startswith("flan"):
                        rmFile = cmd[3:]
                        if rmFile == "":
                            print("No string provided.")
                        else:
                            os.remove(rmFile)
                    elif cmd.startswith("rmdir"):

                        rmDir = cmd[6:]
                        if rmDir == "":
                            print("No string provided.")
                        else:
                            os.rmdir(rmDir)
                    elif cmd.startswith("su"):
                        user_preInput = cmd[3:]
                        if user_preInput == "":
                            print("Please type you want to login super user.")
                        elif user_preInput == "minqwq":
                            print("If you know the password, please reboot and try to login to this account.")
                        elif user_preInput == "minimalmio" or user_preInput == "MinimalMio" or user_preInput == "Minimal_Mio" or user_preInput == "minimal_mio":
                            print("Sorry, you dont have permission to login to this account, if you want, reboot to login manager.")
                        else:
                            user = user_preInput
                            print("Logged in as " + user)
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
                            print("No string provided...")
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
                        print("CPU Performance Test by minqwq")
                        print("2024-09-07")
                        runPreInstApp(lsh_path_fixed + "/apps/pftest/mark.py")

                    elif cmd == "nekochat":
                        nekochatConnectToIP = input("Input server IP: ")
                        nekochatConnectToPort = input("Input server Port: ")
                        nekochatUsername = input("What's your name?: ")
                        print("Welcome to NekoChat Client(Python Port) by Yukari2024")
                        runPreInstApp(lsh_path_fixed + "/apps/nekochat/py/client.py --ip " + nekochatConnectToIP + " --port " + nekochatConnectToPort + " --name " + nekochatUsername)

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

                    elif cmd == "ping": # Ping tool
                        pingToolIPInput = input("Input IP or Domain: ")
                        pingToolCountInput = input("Send how many packages: ")
                        os.system("ping -c " + pingToolCountInput + " " + pingToolIPInput)

                    elif cmd == "hostname":
                        print("add option -c to change.\n\nHostname:\n" + lsh_hostname)
                    elif cmd == "hostname -c":
                        lsh_hostname_pre = input("> ")
                        if lsh_hostname_pre == "":
                            print("No string provided.")
                        else:
                            lsh_hostname = lsh_hostname_pre

                    elif cmd.startswith("sudo"): # sudo not sudo
                        print("This system is not based on linux, so sudo is not on herse")

                    elif cmd.startswith("szk"):
                        # 提取包名，即命令去掉前四个字符后的部分
                        pypkg = cmd[4:]
                        if isWindows == "true":
                            try:
                                os.chdir(".\\data\\apps\\" + pypkg)
                                os.system("python " + pypkg + ".py")
                            except FileNotFoundError:
                                print("Package not found: " + pypkg)
                                os.chdir(pyosi_local_path)
                            except Exception as e:
                                print("Error: " + str(e))
                                os.chdir(pyosi_local_path)
                            finally:
                                os.chdir(pyosi_local_path)
                        elif isWindows == "false":
                            try:
                                os.chdir(lsh_path_fixed + "/data/apps/" + pypkg)
                                os.system("python " + pypkg + ".py")
                            except FileNotFoundError:
                                print("Package not found: " + pypkg)
                                os.chdir(pyosi_local_path)
                            except Exception as e:
                                print("Error: " + str(e))
                                os.chdir(pyosi_local_path)
                            finally:
                                os.chdir(pyosi_local_path)

                    elif cmd == "about": # About system
                        slowprint("---------------| About |---------------")
                        print(color.blue + "VoidFlan Project " + system_version + " " + system_build + " by Yartmin Scarlet" + color.reset)
                        print("(C) " + color.green + "0x1c Studio " + color.reset + "2022--2023 | (C) " + colorama.Fore.LIGHTRED_EX + "Flandre" + color.red + " Studio " + color.reset + "&" + color.grey + " FCNM " + color.reset + "&" + color.grey + " SnowMio Studios 2022--2025" + color.reset)
                        print("Python version: " + str(platform.python_version()))
                        print(" ")
                        print("add option -c for credits\nadd option -s for support\nadd option -l for license")
                    elif cmd == "about -c" or cmd == "about --credits":
                        print(colorama.Fore.LIGHTCYAN_EX + "Developers of VoidFlan Project" + color.reset)
                        print(colorama.Back.WHITE + colorama.Fore.BLACK + "Developers" + color.reset)
                        print("minqwq | Interface Design, Coder, Project Creator, Document Editer")
                        print("bibimingming | Module Installer")
                        print("MeltedIde aka MeltedIce aka AMDISYES(Original PY OS) | Original Project Creator")
                        print("北橋 桜 aka MinimalMio aka Yukari2024 | Installer(old), Helper")
                        print("Dr. Evan | Installer(new), shizuku v2")
                        print(colorama.Back.WHITE + colorama.Fore.BLACK + "Early developing tester(not sorted)" + color.reset)
                        print("minqwq")
                        print("bibimingming")
                        print("Safari_Browse(Rongxuan2022)")
                        print("MeltedIce aka AMDISYES")
                        print(colorama.Back.WHITE + colorama.Fore.BLACK + "Special Thanks for these projects" + color.reset)
                        print("https://github.com/shkolovy/tetris-terminal | Used for games")
                        print("https://github.com/pipeseroni/pipes.sh | Used for screensaver")
                        print("http://154.64.231.6:3000/Yukari/Minesweeper | Used for games")
                        print("https://github.com/erkankavas/python-rss-reader | RSS Reader")
                        print("https://github.com/alewmoose/2048-in-terminal | Used for games")
                    elif cmd == "about -s" or cmd == "about --support":
                        cat(lsh_path_fixed + "/coreutil/plaintext/before_talking.txt")
                        print("minqwq's social accounts:")
                        print("QQ:3575824194")
                        print("WeChat:minqwq723897")
                        print("E-mail:minqwq723897@outlook.com")
                        print("Telegram:@minqwq723897")
                        print("IRC(Instant only):minqwq #pyos-improved irc.freenode.net:6667")
                        print("AutumnChat:Unavailable")
                    elif cmd == "about -l":
                        cat(lsh_path_fixed + "/LICENSE")

                    elif cmd == "power":
                        print("Power options:")
                        print("Shutdown:shutdown or without start by power, st")
                        print("Restart:reboot or without start by power, rbt")
                        print(" ")
                        print("ex:power reboot")
                    elif cmd == "power shutdown" or cmd == "st" or cmd == ":q" or cmd == "halt": # Shutdown
                        logger.info("Shutting down...")
                        clearScreen()
                        for i in range(175):
                            print(colorama.Back.LIGHTWHITE_EX)
                            time.sleep(0.0005)
                        print(color.reset)
                        clearScreen()
                        input("You can safe turn off your computer now.(any key...)")
                        clearScreen()
                        sys.exit()
                    elif cmd == "power reboot" or cmd == "reboot":
                        visuallog("Executing reboot process...", 0)
                        visuallog("Unloading all modules and kernel...", 1)
                        '''
                        for tmp_module0 in set(sys.modules.keys()):
                            if tmp_module0 not in sys.buildin_module_names and not tmp_module0.startswith("_"):
                                del sys.modules[tmp_module0]
                        '''
                        visuallog("Unloaded complete...", 0)
                        visuallog("Reset Spell \"Reboot the world\"", 0)
                        time.sleep(1)
                        clearScreen()
                        goto(line=1)

                    elif cmd == "screensaver": # Screensaver
                        os.chdir(lsh_path_fixed + "/apps/_screensaver")
                        runPreInstApp("scrsv.py")
                        os.chdir("../..")

                    elif cmd == "tetris":
                        print("   #####   ####  #####   ###    #   ####")
                        print("     #     #       #     #  #      #")
                        print(" *   #     ###     #     # #    #   ###   *")
                        print("     #     #       #     #  #   #      #")
                        print("     #     ####    #     #   #  #  ####")
                        print(" ")
                        print("by shkolovy")
                        print("https://github.com/shkolovy/tetris-terminal")
                        time.sleep(3)
                        runPreInstApp(lsh_path_fixed + "/apps/tetris/tetris.py")

                    elif cmd == "time": # Show current time
                        now = datetime.datetime.now()
                        other_StyleTime = now.strftime("%b %a %d %H:%M:%S %Y")
                        print(other_StyleTime)
                        
                    elif cmd == "caesar":
                        os.chdir(lsh_path_fixed + "/apps/caesartools")
                        runPreInstApp("caesar.py")
                        os.chdir("../..")

                    elif cmd == "cuscmd":
                        print("Type custom command below...(ex:cat ciallo.txt)")
                        customCommand = input("")
                        if "sudo" in customCommand:
                            cc_chksudo = input("Are you sure to use sudo?[Enter/Another(no)]")
                            if cc_chksudo == "":
                                os.system(customCommand)
                            else:
                                pass
                        else:
                            os.system(customCommand)

                    elif cmd == "tutor":
                        os.chdir(lsh_path_fixed + "/apps/tutor")
                        runPreInstApp("tutor.py")
                        os.chdir("../..")

                    elif cmd == "": # what is this??? --minqwq at 2024-06-12 19:32
                        space = "0"

                    elif cmd == "clear": # Clear screen using real system command
                        clearScreen()

                    elif cmd == "exit": # Logout
                        clearScreen()
                        systemIsLocked = True
                        print("VoidFlan " + system_version + " (Locked.)")
                        print("Press u and press enter to login account...")
                        print("or...\ntime   | View current time")
                        print("st   | Shutdown")
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
                        if rsyscmd_when_cnf == "true":
                            print("Unknown command, rsyscmd_when_cnf is enabled so will try to run external command...")
                            os.system(cmd)
                        elif rsyscmd_when_cnf == "false":
                            beep()
                            visuallog("Command not found on the list m(__)m : " + cmd, 2)
                            print(color.red + "[Unknown command]" + color.reset, end=' ')
                            logger.error("tty1/lsh | " + cmd + " | Command not found!")
            except KeyboardInterrupt: # Ctrl+C, "Ctrl+Alt+Del" like action
                try:
                    print("\nPress 1 to restart\nPress other key to back\nor Press Ctrl+C again to shutdown...")
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
                time.sleep(0.1)
                beep()
                time.sleep(0.1)
                beep()
                clearScreen()
                traceback.print_exception(crashReason, limit=1145, file=sys.stdout)
                cat(lsh_path_fixed + "/coreutil/buildtime_styled.txt")
                runPreInstApp("coreutil/catchinfo.py")
                print("Last command input " + cmd)
                visuallog("System Panic o(╥﹏╥)o : な、何か予期しないエラーが発生しましたにゃ (⁄ ⁄•⁄ω⁄•⁄ ⁄)", 3)
                input("[Press any key to shutdown - " + str(crashReason) + "]")
                clearScreen()
                sys.exit()
        if logout == True:
            break
        elif logout == False:
            pass
