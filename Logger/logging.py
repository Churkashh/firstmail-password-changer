from colorama import Fore
import datetime

blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
yellow = Fore.YELLOW
black = Fore.LIGHTBLACK_EX
basic = Fore.RESET


def success(msg: str, email: str, status: int):
    print(f"{black}{datetime.datetime.now().strftime("%I:%M:%S %p")} ~ {blue}[FIRSTMAIL-CHANGER]{black} ~{green} {msg} {black}Email={basic}{email} {black}Status={basic}{status}")
    

def error(msg: str, email: str, status=None):
    print(f"{black}{datetime.datetime.now().strftime("%I:%M:%S %p")} ~ {blue}[FIRSTMAIL-CHANGER]{black} ~{red} {msg} {black}Email={basic}{email} {black}Status={basic}{status}")


def ratelimit(msg: str, email: str, status: int):
    print(f"{black}{datetime.datetime.now().strftime("%I:%M:%S %p")} ~ {blue}[FIRSTMAIL-CHANGER]{black} ~{yellow} {msg} {black}Mail={basic}{email} {black}Status={basic}{status}")
