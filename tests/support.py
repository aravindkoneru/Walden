from pathlib import Path

from walden._data_classes import WaldenConfiguration
from walden._config import _parse_walden_config


def good_config(base_path: Path, journal_info: dict = {}) -> WaldenConfiguration:
    config = {
        "config_path": base_path / ".config" / "walden.conf",
        "default_journal_path": base_path / "journals",
        "journals": {},
    }

    for name, path in journal_info.items():
        config["journals"][name] = config["default_journal_path"] / path

    return _parse_walden_config(config)


def create_journal_fs(journal_path: Path):
    years = [f"202{x}" for x in range(0, 9)]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    entries = [f"{x}.tex" for x in range(10, 15)]

    fs_base = journal_path / "entries"
    fs_base.mkdir(parents=True, exist_ok=False)

    for year in years:
        year_base = fs_base / year
        year_base.mkdir()

        for month in months:
            month_base = year_base / month
            month_base.mkdir()

            (year_base / f"{month}.tex").write_text(f"{month} collection")

            for entry in entries:
                (month_base / entry).write_text(f"{year}/{month}/{entry} entry")
