# ScarletInstaller 1.0.1
# License:minqwq's License 1.0
# by Flandre Studio aka minqwq

import os

program_name = "VoidFlan Project II"
print("Scarlet Software Installer | by Flandre Studio")
print("Welcome to " + program_name + " Installer!")
print("This program let you install " + program_name + " completely.")

print("Step 1: " + "Install Python modules")
choice01 = input("Normally install:*Press enter*\n(dangerous) Add --break-system-packages:B\nAdd custom parameter:C\nUse venv:V\n[None/B/C/V]")
if choice01 == "":
    os.system("pip install -r requirements.txt")
elif choice01 == "B" or choice01 == "b":
    os.system("pip install -r requirements.txt " + "--break-system-packages")
elif choice01 == "V" or choice01 == "v":
    choice02 = input("Path to pip at your venv(example:~/pyvenv/bin/pip): ")
    os.system(choice02 + " install -r requirements.txt")
elif choice01 == "C" or choice01 == "c":
    while True:
        para01 = input("Custom parameter: ")
        print("Press enter will run this command and go to next step:")
        print("pip install -r requirements.txt " + para01)
        yorn01 = input("Continue?[Y/N]")
        if yorn01 == "Y" or yorn01 == "y":
            os.system("pip install -r requirements.txt " + para01)
            break
        elif yorn01 == "N" or yorn01 == "n":
            pass
print("Install finished.")
