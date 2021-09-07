import shutil

from ._data_classes import WaldenConfiguration
from ._errors import WaldenException
from ._utils import print_success

SUCCESS = 0


def delete_journal(journal_name: str, config: WaldenConfiguration) -> int:
    journal_name = journal_name[0]

    # TODO: add a confirmation before deleting?
    # TODO: consider case where deletion succeeds but config save fails

    # everything in here is a transaction
    try:
        journal_path = config.journals[journal_name].path

        if journal_path.exists():
            shutil.rmtree(journal_path)

        del config.journals[journal_name]
        config.save()

        print_success(f"Deleted '{journal_name}'!")

    except Exception as e:
        raise e

    return SUCCESS
