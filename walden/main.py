import argparse
import os
import sys
from collections import namedtuple
from pathlib import Path

import toml

from ._build import build_journal
from ._create import create_journal
from ._data_classes import JournalConfiguration, WaldenConfiguration
from ._delete import delete_journal
from ._edit import edit_journal
from ._errors import WaldenException
from ._list import list_journals
from ._utils import print_error

# for initializing commands that need journal name
ARGUMENTS = [
    ("create", "create a new journal"),
    ("today", "edit today's entry"),
    ("delete", "delete specified journal"),
    ("build", "compile the specified journal"),
    ("view", "open the specified journal (OS dependent)"),
]

# for initializing flags
FLAGS = [
    ("list", "list all journals managed by walden"),
]

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

    for cmd, help_txt in ARGUMENTS:
        ex_group.add_argument(
            f"-{cmd[0]}",
            f"--{cmd}",
            type=str,
            nargs=1,
            help=help_txt,
            metavar="JOURNAL_NAME",
        )

    for flag, help_txt in FLAGS:
        ex_group.add_argument(
            f"-{flag[0]}",
            f"--{flag}",
            action="store_true",
            help=help_txt,
        )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def _create_walden_config(config_file_path: Path):
    """Write default configuration file at specified path"""

    config = {
        "walden": {
            "config_path": str(config_file_path),
            "default_journal_path": str(Path.home() / "journals"),
        }
    }

    config_file_path.write_text(toml.dumps(config))


def _validate_config(config: dict):
    """ensure that required fields are in config"""

    if not config.get("walden", {}).get("config_path"):
        raise WaldenException("Missing 'config_path' in walden configuration")

    if not config["walden"].get("default_journal_path"):
        raise WaldenException("Missing 'default_journal_path' in walden configuration")


def _parse_walden_config(config: dict) -> WaldenConfiguration:
    """Parse raw configuration into a dataclass for easier access"""

    config_path, default_journal_path = Path(config["config_path"]), Path(
        config["default_journal_path"]
    )
    journal_info = {}
    for journal_name, info in config.items():
        if journal_name == "config_path" or journal_name == "default_journal_path":
            continue

        journal_info[journal_name] = JournalConfiguration(
            name=journal_name, path=Path(info["path"])
        )

    return WaldenConfiguration(
        config_path=config_path,
        default_journal_path=default_journal_path,
        journals=journal_info,
    )


def _get_config() -> WaldenConfiguration:
    """Create configuration if it doesn't exist and return an object representing the config"""

    config_dir = Path.home() / ".config" / "walden"
    config_dir.mkdir(parents=True, exist_ok=True)

    # config file is stored as a toml
    config_file_path = config_dir / "walden.conf"

    if not config_file_path.exists():
        _create_walden_config(config_file_path)

    config = toml.load(config_file_path)

    _validate_config(config)

    return _parse_walden_config(config["walden"])


def main():
    """Parse arguments, fetch config, and route command to appropriate function"""

    try:
        args = _parse_args()
        config = _get_config()

        cmd, value = next(
            (cmd, value) for cmd, value in vars(args).items() if value != None
        )

        # check if command is a flag
        if value == True:
            sys.exit(FLAG_MAPPING[cmd](config))

        if cmd in ["build", "delete", "view", "today"]:
            # verify journal exists and is accessible
            journal_name = value[0]
            journal_info = config.journals.get(journal_name)

            if not journal_info:
                raise WaldenException(
                    f"'{journal_name}' not found! Please create a journal before attempting to access it."
                )

            journal_path = journal_info.path

            if not journal_path.exists():
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
