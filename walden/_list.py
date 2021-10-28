from ._data_classes import WaldenConfiguration
from ._utils import print_success

SUCCESS = 0


def list_journals(config: WaldenConfiguration) -> int:
    journals = list(config.journals.keys())

    if len(journals) == 0:
        print_success("No journals exist yet")
        return SUCCESS

    print_success("List of journals: ")
    print("\n".join(journals))

    return SUCCESS
