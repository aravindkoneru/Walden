import shutil

from ._data_classes import WaldenConfiguration
from ._errors import WaldenException
from ._utils import print_success

SUCCESS = 0


def delete_journal(journal_name: str, config: WaldenConfiguration) -> int:
    journal_name = journal_name[0]

    # verify that journal exists
    journal_info = config.journals.get(journal_name)

    if not journal_info:
        raise WaldenException(
            f"No journal named '{journal_name}' found in configuration!"
        )

    # everything in here is a transaction
    try:
        journal_path = journal_info.path

        if journal_path.exists():
            shutil.rmtree(journal_path)

        del config.journals[journal_name]
        config.save()

        print_success(f"Deleted '{journal_name}'!")

    except Exception as e:
        raise e

    return SUCCESS