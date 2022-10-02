from typing import Optional, List

from walden._errors import WaldenException
from walden._data_classes import WaldenConfiguration, JournalConfiguration

from walden._config import get_config


class WaldenAPI:
    def __init__(self, config: WaldenConfiguration):
        self._config = config

    def get_journal_info(self, journal_name: str) -> JournalConfiguration:
        if journal := self._config.get_journal(journal_name):
            return journal

        raise WaldenException("Failed to find {journal_name}. Are you sure it exists?")

    def get_journal_entries(
        self, journal_config: JournalConfiguration, year: str = None, month: str = None
    ) -> List[str]:
        """Returns a list with all the top level entries for the specified time period."""

        base_path = journal_config.path / "entries"

        if not year:
            return [file.parts[-1] for file in base_path.iterdir()]

        year_path = base_path / year
        if not year_path.exists():
            raise WaldenException(
                "Failed to fetch entries for {year} in {journal_config.name}"
            )

        if not month:
            return [file.parts[-1] for file in year_path.iterdir() if file.is_dir()]

        month_path = year_path / month
        if not month_path.exists():
            raise WaldenException(
                "Failed to fetch entries for {month}/{year} in {journal_config.name}"
            )

        return [file.parts[-1] for file in month_path.iterdir()]
