from datetime import datetime

from walden.utils import (
    DEFAULT_JOURNAL_PATH,
    sanitize_journal_name,
    print_success,
    print_error,
    print_warning,
    save_journal_metadata,
    get_journal_info,
    get_journal_list
)
from .basic_journal import BasicJournal

JOURNAL_TYPES = [BasicJournal]
JOURNAL_MAP = {j.JOURNAL_TYPE: j for j in JOURNAL_TYPES}

def create_journal(journal_name, journal_type=BasicJournal.JOURNAL_TYPE, base_path=DEFAULT_JOURNAL_PATH):
    """
    Wrapper function to create a journal of a specified type.
    - journal_type will be used to support new journal formats.
    - base_path will be used to support custom per journal locations
    """
    if journal_name in get_journal_list():
        print_warning(f" A journal named: \"{journal_name}\" already exists.")
        return

    journal = JOURNAL_MAP[journal_type](journal_name, base_path)

    if not journal.exists():
        if journal.create() and save_journal_metadata(journal.get_metadata()):
            print_success(f"{journal_name} successfully created!")
            return
        else:
            journal.delete()
            print_error(f"Something went wrong, {journal_name} could not be created.")
            return

def edit_journal_entry(journal_name, date=datetime.now()):
    """
    Wrapper function to edit a journal entry. The default behavior is to edit the current day's
    entry, but date is provided to support the future change of being able to edit any entry.
    """
