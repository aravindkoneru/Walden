from typing import List

from ._data_classes import WaldenConfiguration

SUCCESS = 0
FAILURE = 1


def create_journal(journal_name: List[str], config: WaldenConfiguration) -> int:
    print(journal_name)

    return SUCCESS
