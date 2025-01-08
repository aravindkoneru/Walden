from pathlib import Path

import toml

from ._data_classes import JournalConfiguration, WaldenConfiguration
from ._errors import WaldenException


def _create_walden_config(config_file_path: Path):
    """Write default configuration file at specified path"""

    config = {
        "walden": {
            "config_path": str(config_file_path),
            "default_journal_path": str(Path.home() / "journals"),
            "journals": {},
        }
    }

    config_file_path.parents[0].mkdir(parents=True, exist_ok=False)
    config_file_path.write_text(toml.dumps(config))


def _validate_config(config: dict):
    """ensure that required fields are in config"""

    if not "walden" in config:
        raise WaldenException("Unkown walden configuration file format")

    if not config["walden"].get("config_path"):
        raise WaldenException("Missing 'config_path' in walden configuration")

    if not config["walden"].get("default_journal_path"):
        raise WaldenException("Missing 'default_journal_path' in walden configuration")

    if "journals" not in config["walden"]:
        raise WaldenException("Missing 'journals' in walden configuration")


def _parse_walden_config(config: dict) -> WaldenConfiguration:
    """Parse raw configuration into a dataclass for easier access"""

    config_path Path(config["config_path"])
    default_journal_path = Path(config["default_journal_path"])

    journal_info = {
        j_name: JournalConfiguration(j_name, Path(j_path))
        for j_name, j_path in config["journals"].items()
    }

    return WaldenConfiguration(
        config_path=config_path,
        default_journal_path=default_journal_path,
        journals=journal_info,
    )


def _get_config() -> WaldenConfiguration:
    """Create configuration if it doesn't exist and return an object representing the config"""

    # config file is stored as a toml
    config_file_path = Path.home() / ".config" / "walden" / "walden.conf"

    if not config_file_path.exists():
        _create_walden_config(config_file_path)

    config = toml.load(config_file_path)

    _validate_config(config)

    return _parse_walden_config(config["walden"])


def get_config() -> WaldenConfiguration:
    return _get_config()
