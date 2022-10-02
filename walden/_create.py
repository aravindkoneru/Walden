import shutil
from pathlib import Path
from typing import List

from ._data_classes import JournalConfiguration, WaldenConfiguration
from ._errors import WaldenException
from ._utils import print_success, sanitize_journal_name

SUCCESS = 0


def _gen_new_aux_page(label: str, is_title: bool) -> str:
    """Generate latex for auxillary pages"""

    page = []

    if is_title:
        page.append("\\thispagestyle{empty}")

    page.append("\\begin{center}")
    page.append("\t\\vfil")
    page.append("\t\\vspace*{0.4\\textheight}\n")
    page.append("\t\\Huge")
    page.append(f"\t\\bf{{{label}}}\n")
    page.append("\t\\normalsize")
    page.append("\\end{center}")

    return "\n".join(page)


def _create_page_templates(path: Path, journal_name: str):
    """Write auxillary latex files to disk"""

    files = [
        ("newmonth.tex", "\\month"),
        ("newyear.tex", "\\year"),
        ("title.tex", journal_name),
    ]

    aux_dir = path / "aux"
    aux_dir.mkdir()

    [
        (aux_dir / file[0]).write_text(_gen_new_aux_page(file[1], "title" in file[1]))
        for file in files
    ]


def create_journal(journal_name: List[str], config: WaldenConfiguration) -> int:
    """Responsbile for creating a new journal"""

    journal_name = journal_name[0]

    # check that journal with same name doesn't already exist
    if journal_name in config.journals:
        raise WaldenException(f"Journal named {journal_name} already exists!")

    # ensure no path conflict due to naming
    journal_path = config.default_journal_path / sanitize_journal_name(journal_name)
    if journal_path.exists():
        raise WaldenException(
            f"Tried to create new journal at {journal_path}, but path already exists!"
        )

    # everything inside here is a transaction
    try:
        # create path to journal
        journal_path.mkdir(parents=True)

        # create aux files
        _create_page_templates(journal_path, journal_name)

        # create new SchemaConfiguration and save walden config
        config.add_journal(journal_name, journal_path)
        config.save()

        print_success(f"Created journal named '{journal_name}' at {journal_path}!")

    except Exception as e:
        # remove journal from disk
        if journal_path.exists():
            shutil.rmtree(journal_path)

        # remove from configuration
        if journal_name in config.journals:
            del config.journals[journal_name]

        raise e

    return SUCCESS
