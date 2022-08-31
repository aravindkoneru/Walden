from pathlib import Path
import toml

from ._errors import WaldenException
from ._data_classes import JournalConfiguration, WaldenConfiguration


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
    for journal_name, journal_path in config.items():
        if journal_name == "config_path" or journal_name == "default_journal_path":
            continue

        journal_info[journal_name] = JournalConfiguration(
            name=journal_name, path=Path(journal_path)
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


def get_config() -> WaldenConfiguration:
    return CONFIG


CONFIG: WaldenConfiguration = _get_config()
