import sys

from colorama import Fore, init

init(autoreset=True)


def print_error(msg: str):
    print(Fore.RED + f"{msg}", file=sys.stderr)


def print_success(msg: str):
    print(Fore.GREEN + msg)
