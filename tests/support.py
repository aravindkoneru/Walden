from pathlib import Path

from walden._data_classes import WaldenConfiguration
from walden._config import _parse_walden_config


def good_config(base_path: Path, journal_info: dict = {}) -> WaldenConfiguration:
    config = {
        "config_path": base_path / ".config" / "walden.conf",
        "default_journal_path": base_path / "journals",
    }

    for name, path in journal_info.items():
        config[name] = config["default_journal_path"] / path
        print(config[name])

    return _parse_walden_config(config)
