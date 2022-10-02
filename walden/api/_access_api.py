from typing import Optional

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
