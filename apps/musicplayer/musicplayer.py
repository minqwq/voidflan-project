import colorama
import os
try:
    from goto import goto
except ModuleNotFoundError:
    from python_goto import goto
class color: # Text colors
    red = "\033[31m"
    green = "\033[32m"
    blue = "\033[34m"
    yellow = "\033[33m"
    purple = "\033[35m"
    cyan = "\033[36m"
    grey = "\033[37m"
    reset = "\033[0m"
print("v2.2")
print("How to play:<type> play" + color.cyan + " *Enter*" + color.reset)
print("Available type:mod, sid, mpeg")
print("For internal musics list, type list to get a list")
print("mpeg requires the internet to play, because the mp3 is in minqwq's personal site")
print("exit:exit")
print(" ")
var = 1
while var == 1:
    cmd = input("\n> ")
    if cmd == "mod play":
        i = os.system("ls ../../music/modulemusic")
        mpModulePlay = input("Type a music filename: ")
        i = os.system("openmpt123 --quiet ../../music/modulemusic/" + mpModulePlay)
    elif cmd == "sid play":
        i = os.system("ls ../../music/sid")
        mpSIDPlay = input("Type a music filename: ")
        i = os.system("sidplayfp -q ../../music/sid/" + mpSIDPlay)
    elif cmd == "mpeg play":
        isNet = input("Do you have internet?\n1:Yes\n2:No\n>  ")
        if isNet == "2":
            goto(lines=17)
        i = os.system("cat ./mpeglist.txt")
        mpMPEGPlay = input("Type a music filename: ")
        i = os.system("mpg123 -q https://minqwq.us.kg/audio/mp3_64kbps/" + mpMPEGPlay)
    elif cmd == "list":
        print("musicname <type> play filename")
        print(colorama.Fore.BLACK + colorama.Back.WHITE + "Module(xm, mod, s3m)" + color.reset)
        i = os.system("ls ../../music/modulemusic/")
        print(colorama.Fore.BLACK + colorama.Back.WHITE + "SID(Commodore 64/128)" + color.reset)
        i = os.system("ls ../../music/sid/")
        print(colorama.Fore.BLACK + colorama.Back.WHITE + "MPEG" + color.reset)
        i = os.system("ls ../../music/mpeg/")
    elif cmd == "exit":
        exit()
    else:
        print("?")
