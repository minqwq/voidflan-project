"""
# PY OS Improved Installer Version 2.0
# License: minqwq's License 1.0
# By Dan_Evan aka ElofHew
@ Website: http://www.drevan.xyz/
@ Github: https://github.com/ElofHew/
@ Bilibili: https://space.bilibili.com/642688364/
$ Lastest Update: 2025/05/01
"""

# 导入模块
import os,time,sys,subprocess,platform,json

# 选择语言
print("    Choose Languages    ")
print("------------------------")
print("1. English（US & UK）")
print("2. 简体中文（中国大陆）")
print("3. 繁体中文（港/澳/台）")
print("4. 日本語（日本）")
print("5. Русский (Россия)")
print("------------------------")
while True:
    lang = str(input("> "))
    if str(lang) == "1":
        print("Welcome to PY OS Improved Installer!\n")
        break
    elif str(lang) == "2":
        print("欢迎使用PY OS Improved安装程序！\n")
        break
    elif str(lang) == "3":
        print("歡迎使用PY OS Improved安裝程式！\n")
        break
    elif str(lang) == "4":
        print("ようこそPY OS Improvedインストーラへ！\n")
        break
    elif str(lang) == "5":
        print("Добро пожаловать в PY OS Improved инсталлятор!\n")
        break
    else:
        print("Invalid input. Please choose a number from the list.\n")
        continue

# 定义不同语言的变量
program_name = "PY OS Improved"
if lang == "1":
    input_error = "Invalid input, please try again."
    text_01 = "Scarlet Package Installer | Flandre Studio Production"
    text_02 = "Welcome to " + program_name + " Installer!"
    text_03 = "This program can install " + program_name + " completely."
    step0_0 = "Preparation: Setting pip mirror source"
    step0_2 = "Updating pip"
    step0_3 = "Current pip version:"
    step0_4 = "Switching pip mirror source..."
    step0_5 = "Switched pip mirror source to Tsinghua University mirror source"
    step0_6 = "Switched pip mirror source to pypi official source"
    step1_0 = "Step 1: Install Python modules"
    step1_1 = "[1]General Install\n[2]Use --break-system-packages (Dangerous Option)\n[3]Add Custom Parameters\n[4]Use venv"
    step1_2 = "Please enter your venv's pip path (e.g. ~/pyvenv/bin/pip): "
    step1_3 = "Please enter your custom parameters:\n"
    step1_4 = "Press Enter to run this command and go to the next step, input N and Enter to cancel:"
    step1_5 = "Custom parameters are incorrect, please re-enter"
    step2_0 = "Step 2: Check module installation success"
    step2_1 = "Uninstalled modules:"
    step2_2 = "All modules have been installed."
    step2_3 = "Failed to install modules, you can manually enter “pip install module_name” to install them, or re-run this installer again"
    step2_4 = "(Assuming you have correctly installed pip)"
    step3_0 = "Step 3: Configure PY OS Improved"
    step3_1 = "Detecting your operating system as Windows, is this correct? Yes = Enter, No = Enter any character and Enter"
    step3_2 = "Detecting your operating system as Linux/macOS (not Windows), is this correct? Yes = Enter, No = Enter any character and Enter"
    step3_3 = "Completed PY OS Improved configuration for Windows operating system."
    step3_4 = "Non-Windows operating system, no modification for Windows operating system."
    step3_5 = "Completed PY OS Improved configuration for non-Windows operating system."
    step3_6 = "Windows operating system, modified for Windows operating system."
    after_install = "Tips:\n[1] If you are using Windows, it is recommended to use cmd or PowerShell to run PY OS Improved.\n[2] If you are using Linux/macOS, you only need to use the terminal to run PY OS Improved.\n[3] If you are using Android, you can use Termux to run PY OS Improved."
    end_text = "For more information, please check the ‘afterinstall.txt’ file.\nInstallation complete, this program will exit in 10 seconds."
elif lang == "2":
    input_error = "无效输入，请重试。"
    text_01 = "Scarlet 软件包安装程序 | Flandre Studio 出品"
    text_02 = "欢迎使用 " + program_name + " 安装程序！"
    text_03 = "这个程序可以让你完全安装 " + program_name + " 。"
    step0_0 = "准备工作：设置pip镜像源"
    step0_1 = "您是否需要将pip的镜像源设置为清华源？\n(我们强烈建议中国大陆用户换源以获得更高速更稳定的下载环境)\n[1]更换清华源/[2]使用/更换pypi默认镜像源(不换源)"
    step0_2 = "正在更新pip"
    step0_3 = "当前pip版本："
    step0_4 = "正在切换pip镜像源..."
    step0_5 = "已将pip镜像源切换至清华大学镜像源"
    step0_6 = "已将pip镜像源切换至pypi官方源"
    step1_0 = "第一步：安装Python模块"
    step1_1 = "[1]常规安装\n[2]使用 --break-system-packages (危险选项)\n[3]添加自定义参数\n[4]使用 venv"
    step1_2 = "请输入你的 venv 中的 pip 的路径(例如:~/pyvenv/bin/pip): "
    step1_3 = "请输入你的自定义参数:\n"
    step1_4 = "按下回车将运行这个命令并进入下一步，输入N并回车以取消："
    step1_5 = "自定义参数有误，请重新输入"
    step2_0 = "第二步，检查模块安装是否成功"
    step2_1 = "未安装的模块："
    step2_2 = "所有模块均已安装。"
    step2_3 = "安装失败的模块可手动终端输入“pip install 模块名”来安装，也可以重新运行一遍本安装程序"
    step2_4 = "(前提是确保你已经正确安装了pip)"
    step3_0 = "第三步：配置PY OS Improved"
    step3_1 = "检测到您的操作系统为Windows，是否正确？是 = 回车、否 = 输入任意字符并回车"
    step3_2 = "检测到您的操作系统为Linux/macOS（非Windows），是否正确？是 = Enter、否 = 输入任意字符并Enter"
    step3_3 = "已完成应用于Windows操作系统的PY OS Improved配置项。"
    step3_4 = "非Windows操作系统，未修改针对于Windows操作系统的PY OS Improved配置项。"
    step3_5 = "已完成应用于非Windows操作系统的PY OS Improved配置项。"
    step3_6 = "Windows操作系统，已修改针对于Windows操作系统的PY OS Improved配置项。"
    after_install = "提示:\n[1] 如果您使用Windows，建议您使用cmd或PowerShell运行PY OS Improved。\n[2] 如果您使用Linux/macOS，只需要使用终端运行PY OS Improved。\n[3] 如果您使用Android，您可以使用Termux运行PY OS Improved。"
    end_text = "更多信息请查看‘afterinstall.txt’文件。\n安装完成，本程序将在10秒后退出。"
elif lang == "3":
    input_error = "無效輸入，請重試。"
    text_01 = "Scarlet 套件安裝程式 | Flandre Studio 製造"
    text_02 = "歡迎使用 " + program_name + " 安裝程式！"
    text_03 = "這個程式可以讓您完全安裝 " + program_name + " 。"
    step0_0 = "準備工作：設定pip镜像源"
    step0_2 = "正在更新pip"
    step0_3 = "當前pip版本："
    step0_4 = "正在切換pip镜像源..."
    step0_5 = "已將pip镜像源切換至清華大學镜像源"
    step0_6 = "已將pip镜像源切換至pypi官方源"
    step1_0 = "第一步：安裝Python模組"
    step1_1 = "[1]常規安裝\n[2]使用 --break-system-packages (危險選項)\n[3]加入自定義參數\n[4]使用 venv"
    step1_2 = "請輸入您的 venv 中的 pip 的路徑(例如:~/pyvenv/bin/pip): "
    step1_3 = "請輸入您的自定義參數:\n"
    step1_4 = "按下Enter將執行這個命令並進入下一步，輸入N並Enter以取消："
    step1_5 = "自定義參數有誤，請重新輸入"
    step2_0 = "第二步，檢查模組安裝是否成功"
    step2_1 = "尚未安裝的模組："
    step2_2 = "所有模組均已安裝。"
    step2_3 = "安裝失敗的模組可手動終端輸入“pip install 模組名”來安裝，也可以重新執行本安裝程式"
    step2_4 = "(前提是確保你已經成功安裝了pip)"
    step3_0 = "第三步：設定PY OS Improved"
    step3_1 = "偵測到您的作業系統為Windows，是否正確？是 = Enter、否 = 輸入任意字元並Enter"
    step3_2 = "偵測到您的作業系統為Linux/macOS（非Windows），是否正確？是 = Enter、否 = 輸入任意字元並Enter"
    step3_3 = "已完成應用於Windows作業系統的PY OS Improved設定項。"
    step3_4 = "非Windows作業系統，未修改針對Windows作業系統的PY OS Improved設定項。"
    step3_5 = "已完成應用於非Windows作業系統的PY OS Improved設定項。"
    step3_6 = "Windows作業系統，已修改針對Windows作業系統的PY OS Improved設定項。"
    after_install = "提示:\n[1] 如果您使用Windows，建議您使用cmd或PowerShell執行PY OS Improved。\n[2] 如果您使用Linux/macOS，只需要使用終端執行PY OS Improved。\n[3] 如果您使用Android，您可以使用Termux執行PY OS Improved。"
    end_text = "更多資訊請查看‘afterinstall.txt’檔案。\n安裝完成，本程式將在10秒後退出。"
elif lang == "4":
    input_error = "無効な入力です。リストの番号を選んでください。"
    text_01 = "Scarlet パッケージ インストーラ | Flandre Studio 製作"
    text_02 = "ようこそ " + program_name + " インストーラへ！"
    text_03 = "このプログラムは " + program_name + " を完全にインストールすることができます。"
    step0_0 = "準備作業：pip リモートソースの設定"
    step0_2 = "pip の更新"
    step0_3 = "現在の pip バージョン："
    step0_4 = "pip リモートソースの切り替え中..."
    step0_5 = "pip リモートソースを清华大学リモートソースに切り替えました"
    step0_6 = "pip リモートソースを pypi 公式ソースに切り替えました"
    step1_0 = "ステップ 1：Python モジュールのインストール"
    step1_1 = "[1]一般インストール\n[2] --break-system-packages (危険なオプション)を使用\n[3]カスタムパラメータの追加\n[4]venv の使用"
    step1_2 = "venv の pip のパスを入力してください (例: ~/pyvenv/bin/pip): "
    step1_3 = "カスタムパラメータを入力してください:\n"
    step1_4 = "Enter キーを押してこのコマンドを実行し、次のステップに進みます。N を入力して Enter キーを押すと、インストールをキャンセルします："
    step1_5 = "カスタムパラメータが正しくありません。もう一度入力してください。"
    step2_0 = "ステップ 2：モジュールのインストール成功確認"
    step2_1 = "アンインストールされたモジュール："
    step2_2 = "すべてのモジュールがインストールされています。"
    step2_3 = "モジュールのインストールに失敗しました。手動で “pip install module_name” を入力してインストールすることもできます。もう一度このインストーラーを実行してください。"
    step2_4 = "(前提は pip のインストールが正しく行われていること)"
    step3_0 = "ステップ 3：PY OS Improved の設定"
    step3_1 = "Windows 作業環境を検出しました。正しいですか？ Yes = Enter、No = 任意の文字を入力して Enter"
    step3_2 = "Linux/macOS (非 Windows) 作業環境を検出しました。正しいですか？ Yes = Enter、No = 任意の文字を入力して Enter"
    step3_3 = "Windows 作業環境用の PY OS Improved 設定が完了しました。"
    step3_4 = "非 Windows 作業環境用の PY OS Improved 設定はありません。"
    step3_5 = "非 Windows 作業環境用の PY OS Improved 設定が完了しました。"
    step3_6 = "Windows 作業環境用の PY OS Improved 設定が変更されました。"
    after_install = "ヒント:\n[1] Windows を使用している場合、PY OS Improved を実行する際は、cmd または PowerShell を推奨します。\n[2] Linux/macOS (非 Windows) を使用している場合、PY OS Improved を実行する際は、ターミナルだけで構いません。\n[3] Android を使用している場合、Termux を使用して PY OS Improved を実行することができます。"
    end_text = "詳細情報は「afterinstall.txt」ファイルを確認してください。\nインストールが完了しました。10秒後にこのプログラムは終了します。"
elif lang == "5":
    input_error = "Неверный ввод, пожалуйста, попробуйте еще раз."
    text_01 = "Scarlet пакет установщик | Flandre Studio производство"
    text_02 = "Приветствуем в " + program_name + " инсталляторе!"
    text_03 = "Этот программный комплект позволяет полностью установить " + program_name + " ."
    step0_0 = "Подготовка: установка pip источника"
    step0_2 = "Обновление pip"
    step0_3 = "Текущая версия pip:"
    step0_4 = "Переключение pip источника..."
    step0_5 = "Переключен pip источник на Tsinghua University источник"
    step0_6 = "Переключен pip источник на pypi официальный источник"
    step1_0 = "Шаг 1: Установка Python модулей"
    step1_1 = "[1]Обычная установка\n[2]Использование --break-system-packages (опасный вариант)\n[3]Добавление пользовательских параметров\n[4]Использование venv"
    step1_2 = "Пожалуйста, введите путь к pip в вашем venv (например: ~/pyvenv/bin/pip): "
    step1_3 = "Пожалуйста, введите пользовательские параметры:\n"
    step1_4 = "Нажмите Enter, чтобы выполнить эту команду и перейти к следующему шагу. Введите N и Enter, чтобы отменить установку:"    
    step1_5 = "Неверные пользовательские параметры, пожалуйста, введите их еще раз."
    step2_0 = "Шаг 2: Проверка успешности установки модулей"
    step2_1 = "Отсутствующие модули:"
    step2_2 = "Все модули успешно установлены."
    step2_3 = "Ошибка при установке модулей. Вы можете вручную ввести “pip install module_name” в терминал, чтобы установить модуль, или повторно запустить этот инсталлятор."
    step2_4 = "(Необходимо убедиться, что вы успешно установили pip)"
    step3_0 = "Шаг 3: Настройка PY OS Improved"
    step3_1 = "Обнаружен Windows операционная система. Верно? Yes = Enter, No = введите любой текст и Enter"
    step3_2 = "Обнаружен Linux/macOS (не Windows) операционная система. Верно? Yes = Enter, No = введите любой текст и Enter"
    step3_3 = "Настройка PY OS Improved для Windows завершена."
    step3_4 = "Настройка PY OS Improved для не Windows операционной системы отсутствует."
    step3_5 = "Настройка PY OS Improved для не Windows операционной системы завершена."
    step3_6 = "Настройка PY OS Improved для Windows была изменена."
    after_install = "Подсказка:\n[1] Если вы используете Windows, рекомендуется использовать cmd или PowerShell для запуска PY OS Improved.\n[2] Если вы используете Linux/macOS (не Windows), вам необходимо использовать только терминал для запуска PY OS Improved.\n[3] Если вы используете Android, вы можете использовать Termux для запуска PY OS Improved."
    end_text = "Дополнительную информацию см. в файле 'afterinstall.txt'.\nУстановка завершена. Этот программный комплект завершит свою работу через 10 секунд."

# 定义步骤函数
def pip_ready():
    # 准备工作：针对中国大陆网路环境确认是否对pip进行换源
    print(step0_1)
    while True:
        mirror = str(input("> "))
        if mirror == "1":
            print(step0_2)
            subprocess.run(["python", "-m", "pip", "install", "-i", "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple", "--upgrade", "pip"], check=True)
            # 升级pip至最新版本
            pip_result = subprocess.run(["python", "-m", "pip", "--version"], capture_output=True, text=True)
            print(step0_3, pip_result.stdout)
            # 显示当前pip版本
            time.sleep(1)
            print(step0_4)
            subprocess.run(["pip", "config", "set", "global.index-url", "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"], check=True)
            # 设置pip镜像源
            print(step0_5)
            # 完成设置
            break
        elif mirror == "2":
            print(step0_2)
            subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"], check=True)
            # 升级pip至最新版本
            pip_result = subprocess.run(["python", "-m", "pip", "--version"], capture_output=True, text=True)
            print(step0_3, pip_result.stdout)
            # 显示当前pip版本
            time.sleep(1)
            print(step0_4)
            subprocess.run(["pip", "config", "set", "global.index-url", "https://pypi.org/simple"], check=True)
            # 设置pip镜像源
            print(step0_6)
            # 完成设置
            break
        else:
            print(input_error)
            continue

def step1():
    while True:
        install = str(input("> "))
        if install == "1":
            chk = str(input(step1_4))
            if chk == "N" or chk == "n":
                return step1()
            else:
                subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
                # 常规安装
                break
        elif install == "2":
            if chk == "N" or chk == "n":
                return step1()
            else:
                subprocess.run(["pip", "install", "-r", "requirements.txt", "--break-system-packages"], check=True)
                # 使用 --break-system-packages
                break
        elif install == "3":
            while True:
                custom_args = str(input(step1_3))
                try:
                    subprocess.run(["pip", "install", "-r", "requirements.txt"] + custom_args.split(), check=True)
                    # 添加自定义参数
                    break
                except subprocess.CalledProcessError:
                    print(step1_5)
                    continue
        elif install == "4":
            while True:
                venv_pip_path = str(input(step1_2))
                if os.path.exists(venv_pip_path):
                    break
                else:
                    print(input_error)
                    continue
            if chk == "N" or chk == "n":
                return step1()
            else:
                subprocess.run([venv_pip_path, "install", "-r", "requirements.txt"], check=True)
                # 使用 venv
                break
        else:
            print(input_error)
            continue

def step2(requirements_file='requirements.txt'):
    # 第二步，检查模块安装是否成功
    with open(requirements_file) as f:
        requirements = f.readlines()
    # 打开requirements.txt文件，读取所有内容，并以列表形式存储
    installed_packages = subprocess.check_output([subprocess.sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').split('\n')
    installed_packages = {pkg.split('==')[0].strip().lower() for pkg in installed_packages if pkg}
    # 获取已安装的包
    missing_packages = []
    # 筛选出缺失的包
    for req in requirements:
        req = req.strip()
        if req and not req.startswith('#'):  # 忽略注释
            package_name = req.split('==')[0] if '==' in req else req.split('>')[0] if '>' in req else req.split('<')[0] if '<' in req else req.split('>=')[0] if '>=' in req else req.split('<=')[0] if '<=' in req else req
            # 获取包名
            if package_name.lower() not in installed_packages:
                missing_packages.append(package_name)
                # 筛选出缺失的包
    if missing_packages:
        print(step2_1)
        for package in missing_packages:
            print(package)
        # 显示缺失的包
        time.sleep(1)
        print(step2_3)
        print(step2_4)
        # 部分模块未安装，提示用户手动安装
    else:
        print(step2_2)
        # 成功安装所有模块

def step3():
    # 第三步，区分Windows和非Windows系统，配置PY OS Improved
    if platform.system() == "Windows":
        print(step3_1)
        # 确认当前系统是否为Windows，避免判断错误
        choose02 = input("> ")
        if choose02 == "":
            with open('..\\PYOSI\\system\\config\\config.json', 'r') as file:
                config = json.load(file)
            # 当前系统为Windows，修改配置为true
            config['isWindows'] = True
            with open('..\\PYOSI\\system\\config\\config.json', 'w') as file:
                json.dump(config, file, indent=4)
            print(step3_3)
            # 写入配置文件并提示完成配置
        else:
            with open('../PYOSI/system/config/config.json', 'r') as file:
                config = json.load(file)
            # 当前系统为非Windows，修改配置为false
            config['isWindows'] = False
            with open('../PYOSI/system/config/config.json', 'w') as file:
                json.dump(config, file, indent=4)
            print(step3_4)
            # 写入配置文件并提示未修改配置
    else:
        print(step3_2)
        # 确认当前系统是否为非Windows，避免判断错误
        choose02 = input("> ")
        if choose02 == "":
            with open('../PYOSI/system/config/config.json', 'r') as file:
                config = json.load(file)
            # 当前系统为非Windows，修改配置为false
            config['isWindows'] = False
            with open('../PYOSI/system/config/config.json', 'w') as file:
                json.dump(config, file, indent=4)
            print(step3_5)
            # 写入配置文件并提示完成配置
        else:
            with open('..\\PYOSI\\system\\config\\config.json', 'r') as file:
                config = json.load(file)
            # 当前系统为Windows，修改配置为true
            config['isWindows'] = True
            with open('..\\PYOSI\\system\\config\\config.json', 'w') as file:
                json.dump(config, file, indent=4)
            print(step3_6)
            # 写入配置文件并提示修改配置

time.sleep(1)  # 等待1秒
print(text_01) # 显示标题
print(text_02) # 显示欢迎信息
print(text_03) # 显示欢迎信息
time.sleep(1)  # 等待1秒
print("="*20)  # 分割线
print(step0_0) # 显示准备工作
print("-"*20)  # 分割线
pip_ready()    # 运行准备工作
print("="*20)  # 分割线
print(step1_0) # 显示第一步
print(step1_1) # 显示选项
step1()        # 运行第一步
print("="*20)  # 分割线
print(step2_0) # 显示第二步
time.sleep(1)  # 等待1秒
step2()        # 运行第二步
time.sleep(1)  # 等待1秒
print("="*20)  # 分割线
print(step3_0) # 显示第三步
step3()        # 运行第三步
time.sleep(1)  # 等待1秒
print("="*20)  # 分割线
print(after_install)  # 显示提示信息
print("-"*20)  # 分割线
print(end_text)  # 显示结束信息
time.sleep(10) # 等待10秒
sys.exit()     # 退出程序

# Edit by ElofHew on 2025/04/26