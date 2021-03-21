from walden.utils import (
    sanitize_journal_name,
    print_success,
    print_error,
    print_warning
)
from .basic_journal import BasicJournal

JOURNAL_TYPES = [BasicJournal]
JOURNAL_MAP = {j.JOURNAL_TYPE: j for j in JOURNAL_TYPES}

def create_journal(journal_name, journal_type=BasicJournal.JOURNAL_TYPE):
    journal = JOURNAL_MAP[journal_type](journal_name)

    if not journal.exists():
        if journal.create():
            print_success(f"{journal_name} successfully created!")
        else:
            print_error(f"Something went wrong, {journal_name} could not be created.")
    else:
        print_warning("Sorry journal already exists")
