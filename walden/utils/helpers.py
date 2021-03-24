from colorama import init, Fore

init(autoreset=True)


def sanitize_journal_name(journal_name):
    return journal_name.lower().replace(" ", "_")


def print_success(msg):
    print(Fore.GREEN + f"{msg}")


def print_error(msg):
    print(Fore.RED + f"{msg}")


def print_warning(msg):
    print(Fore.YELLOW + f"{msg}")
