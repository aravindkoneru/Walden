from .base_journal import BaseJournal

class BasicJournal(BaseJournal):
    JOURNAL_TYPE = "BasicJournal"

    def __init__(self, journal_name):
        super().__init__(journal_name)


