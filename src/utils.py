import winreg
import locale
import os
from translate import translate
from colorama import init, Fore, Style
from ctypes import windll
from time import sleep, time
from psutil import process_iter
from script import script
import subprocess

def init_colors():
    init()

def get_steam_path():
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        try:
            steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        except:
            winreg.CloseKey(hkey)
            return ""
        winreg.CloseKey(hkey)
        return steam_path[0]
    except:
        return ""

def get_win_lang():
    return locale.getlocale()

def get_translate(key):
    try:
        lang = get_win_lang()[0]
    except:
        lang = 'en'
    
    if 'ru' in lang.lower():
        lang = 'ru'
    elif 'en' in lang.lower():
        lang = 'en'
    elif 'ch' in lang.lower() or 'cn' in lang.lower():
        lang = 'cn'
    else:
        lang = 'en'
    
    try:
        return translate[key][lang]
    except:
        return ""

def clear():
    os.system('cls')

def run_script(sp):
    ds = script
    with open('C:/rms.bat', 'w', encoding='utf-8') as f:
        f.write(ds.replace('$steam', sp))
    
    st = time()
    result = subprocess.run(['C:/rms.bat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    et = time() - st
    
    try:
        os.remove('C:/rms.bat')
    except:
        pass
    
    return et

def restart():
    os.system('shutdown /r /t 1')

def kill_steam():
    for proc in process_iter():
        if 'dota' in proc.name():
            proc.kill()
        elif 'steam' in proc.name():
            proc.kill()
    sleep(5)

def print_logo():
    logo = [
        "                               ",
        "   .^~~^:             :!77!~.  ",
        "   !~~YJ!^:.........~777J5~7^  ",
        "  .!^~5@G!^!!!!!!~!!7~~5@P^7~  ",
        "  .!^~7@@&Y!7GGP5Y57~J#@@?:7^  ",
        "   !~~!#@@@#Y?P#G57JB@@@&7:!.  ",
        "   ~7~!B@@@@@B?7!?G@@@@@#!~!.  ",
        "   !7!7#@@PB@@@G5&@@#5@@#~!7.  ",
        "   ~7^?&@@Y!B@@@@@@#~?@@&7~!.  ",
        "   7?:J@@@5^!B@@@@#!:J@@@J~~:  ",
        "  ^Y!^5@@@5~~7#@@&?~~J@@@P~!^  ",
        "  7?!~J&@@Y~!~J@@J~!~Y@@&Y^!^. ",
        "   ~!!:?P&J~!!~JY^~!~Y#G?!^~:  ",
        "    .~~!777?J7~!!7!77!!77!~:   ",
        "      .^~~!~:.^^^:.:!!!!~^",
        "                               "
    ]
    
    logo_centred = []
    center = int((os.get_terminal_size().columns - len(logo[0])) / 2)
    
    if center > 2:
        for line in logo:
            logo_centred.append(' ' * center + line)
    else:
        logo_centred = logo
    
    colorfull_logo = []
    for line in logo_centred:
        colorfull_logo.append(line.replace('@', Fore.WHITE + '@' + Fore.LIGHTMAGENTA_EX))
    
    print(Fore.MAGENTA + '\n'.join(logo_centred) + Style.RESET_ALL)
    print("\n    Melonity Spoofer\n    Build by melonity \n    Version: 1.0\n")

def log(text):
    print("    " + text)

def app_is_admin():
    return windll.shell32.IsUserAnAdmin() != 0

def exit():
    sleep(999)
    return 0