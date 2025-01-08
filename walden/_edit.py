import os
from datetime import date
from pathlib import Path
from subprocess import call
from typing import List

from ._data_classes import WaldenConfiguration
from ._errors import WaldenException
from ._utils import print_success

SUCCESS = 0
EDITOR = os.environ.get("EDITOR", "vim")


def _get_new_entry_header() -> str:
    """Return header for new entries"""

    entry = []
    today = date.today()

    entry.append(today.strftime("\\def\\day{\\textit{%B %d, %Y}}"))
    entry.append(today.strftime("\\def\\weekday{\\textit{%A}}"))
    entry.append("\\subsection*{\\weekday, \\day}\n\n")

    return "\n".join(entry)


def generate_entry_path(journal_path: Path, year: str, month: str, day: str) -> Path:
    return journal_path / "entries" / year / month / f"{day}.tex"


def edit_journal(journal_name: List[str], config: WaldenConfiguration) -> int:
    """Create entry for today if it doesn't exist and open it in $EDITOR"""

    journal_name = journal_name[0]
    journal_path = config.get_journal(journal_name).path

    # check to see if new entry needs to be made
    today = date.today()
    entry_path = generate_entry_path(
        journal_path, f"{today.year}", today.strftime("%m"), today.strftime("%d")
    )

    if not entry_path.exists():
        entry_path.parents[0].mkdir(parents=True, exist_ok=True)
        entry_path.write_text(_get_new_entry_header())

    # TODO maybe this could be improved?
    print(f"Opening today's entry for {journal_name}...")
    call([EDITOR, entry_path])
    print_success(f"Finished editing today's entry for {journal_name}!")

    return SUCCESS
