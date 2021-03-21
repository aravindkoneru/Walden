from walden.utils import sanitize_journal_name
from .basic_journal import BasicJournal

JOURNAL_TYPES = [BasicJournal]
JOURNAL_MAP = {j.JOURNAL_TYPE: j for j in JOURNAL_TYPES}

def create_journal(journal_name, journal_type=BasicJournal.JOURNAL_TYPE):
    journal = JOURNAL_MAP[journal_type](journal_name)

    if not journal.exists():
        journal.create()
    else:
        return "Sorry journal already exists"
