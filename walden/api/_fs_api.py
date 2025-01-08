from typing import List, Optional

from walden._config import get_config
from walden._data_classes import JournalConfiguration, WaldenConfiguration
from walden._edit import generate_entry_path
from walden._errors import WaldenException


def _normalize_digits(x: int) -> str:
    """Prepend single digits with '0' to match fs name"""
    return f"0{x}" if x < 10 else f"{x}"


class WaldenFSAPI:
    def __init__(self, config: WaldenConfiguration):
        self._config = config

    def get_journal_info(self, journal_name: str) -> JournalConfiguration:
        if journal := self._config.get_journal(journal_name):
            return journal

        raise WaldenException("Failed to find {journal_name}. Are you sure it exists?")

    def get_journal_hierarchy(
        self, journal_config: JournalConfiguration, year: int = None, month: int = None
    ) -> List[str]:
        """Returns a list with all the top level entries for the specified time period."""

        base_path = journal_config.path / "entries"

        if not year:
            return [file.parts[-1] for file in base_path.iterdir()]

        year_path = base_path / f"{year}"
        if not year_path.exists():
            raise WaldenException(
                "Failed to fetch entries for {year} in {journal_config.name}"
            )

        if not month:
            return [file.parts[-1] for file in year_path.iterdir() if file.is_dir()]

        month_path = year_path / (f"0{month}" if month < 10 else f"{month}")
        if not month_path.exists():
            raise WaldenException(
                "Failed to fetch entries for {month}/{year} in {journal_config.name}"
            )

        return [file.parts[-1] for file in month_path.iterdir()]

    def get_entry(
        self, journal_config: JournalConfiguration, year: int, month: int, day: int
    ) -> str:
        """Returns the text of a specific entry"""
        entry_path = generate_entry_path(
            journal_config.path,
            f"{year}",
            _normalize_digits(month),
            _normalize_digits(day),
        )

        if not entry_path.exists():
            raise WaldenException(
                f"Failed to find entry for {year}/{month}/{day} in {journal_config.name}: {entry_path}"
            )

        return entry_path.read_text()
