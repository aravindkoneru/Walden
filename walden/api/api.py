from ._fs_api import WaldenFSAPI

from walden._config import get_config
from walden._data_classes import WaldenConfiguration, JournalConfiguration

walden_fs_api = WaldenFSAPI(get_config())

def get_journal_info(journal_name: str) -> JournalConfiguration:
    return walden_fs_api.get_journal_info(journal_name)

def get_entry(
        self, journal_config: JournalConfiguration, year: int, month: int, day: int
    ) -> str:
    return walden_fs_api.get_entry(journal_config, year, month, day)


def get_journal_hierarchy(
        self, journal_config: JournalConfiguration, year: int = None, month: int = None
    ) -> List[str]:
    return walden_fs_api.get_journal_hierarchy(journal_config, year, month)
