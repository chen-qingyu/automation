import os
import sys

# check version
if not (sys.version_info.major == 3 and sys.version_info.minor >= 12):
    print("Require at least Python >= 3.12")
    exit(1)

# dynamically load third-party libraries
try:
    import colorama
except ModuleNotFoundError:
    os.system('python -m pip install --upgrade pip setuptools wheel colorama')
    os.system('python -m pip cache purge')
    import colorama

colorama.init(autoreset=True)
COLOR_START = colorama.Fore.BLUE + colorama.Style.BRIGHT
COLOR_INFO = colorama.Fore.CYAN + colorama.Style.BRIGHT
COLOR_FINISH = colorama.Fore.GREEN + colorama.Style.BRIGHT
COLOR_ERROR = colorama.Fore.RED + colorama.Style.BRIGHT
