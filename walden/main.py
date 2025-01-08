import argparse
import os
import sys
from collections import namedtuple
from pathlib import Path

import toml

from ._build import build_journal
from ._config import get_config
from ._create import create_journal
from ._data_classes import JournalConfiguration, WaldenConfiguration
from ._delete import delete_journal
from ._edit import edit_journal
from ._errors import WaldenException
from ._list import list_journals
from ._utils import print_error

# for initializing commands that need journal name
ARGUMENTS = {
    "create": "create a new journal",
    "today": "edit today's entry",
    "delete": "delete specified journal",
    "build": "compile the specified journal",
    "view": "open the specified journal (OS dependent)",
}

# for initializing flags
FLAGS = {
    "list": "list all journals managed by walden"
}

ARGUMENT_MAPPING = {
    "build": build_journal,
    "create": create_journal,
    "delete": delete_journal,
    "today": edit_journal,
    #"view": view_journal
}
FLAG_MAPPING = {"list": list_journals}


def _parse_args() -> argparse.Namespace:
    """Create the arg parser from ARGUMENTS and return the parsed arguments"""

    parser = argparse.ArgumentParser(description="edit and manage your walden journals")
    ex_group = parser.add_mutually_exclusive_group(required=True)

    for cmd, help_txt in ARGUMENTS.items():
        ex_group.add_argument(
            f"-{cmd[0]}",
            f"--{cmd}",
            type=str,
            nargs=1,
            help=help_txt,
            metavar="JOURNAL_NAME",
        )

    for flag, help_txt in FLAGS.items():
        ex_group.add_argument(
            f"-{flag[0]}",
            f"--{flag}",
            action="store_true",
            help=help_txt,
        )

    # no arguments given
    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(1)

    return parser.parse_args()


def main():
    """Parse arguments, fetch config, and route command to appropriate function"""

    try:
        args = _parse_args()
        config = get_config()

        cmd, value = next(
            (cmd, value) for cmd, value in vars(args).items() if value != None
        )

        # check if command is a flag
        if value == True:
            sys.exit(FLAG_MAPPING[cmd](config))

        if cmd in ["build", "delete", "view", "today"]:
            # verify journal exists and is accessible
            journal_name = value[0]
            journal_info = config.get_journal(journal_name)

            if not journal_info:
                raise WaldenException(
                    f"'{journal_name}' not found! Please create a journal before attempting to access it."
                )

            if not journal_info.path.exists():
                raise WaldenException(
                    f"Expected to find '{journal_name}' at {journal_path}, but found nothing!"
                )

        sys.exit(ARGUMENT_MAPPING[cmd](value, config))

    except WaldenException as we:
        print_error(we)
        sys.exit(1)

    except Exception as e:
        raise e
        sys.exit(1)
