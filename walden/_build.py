import os
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from typing import Dict, List

from ._build_log import generate_log
from ._constants import SUCCESS
from ._data_classes import WaldenConfiguration
from ._errors import WaldenException
from ._utils import print_success


def _generate_latex_structure(journal_path: Path):
    """create the aux documents necessary to compile the journal"""

    # aggregate entries by month into a single .tex file
    entries_path = journal_path / "entries"
    entries = _parse_entries(entries_path)

    for year in entries:
        year_path = entries_path / year
        for month in entries[year]:
            monthly_file = year_path / f"{month}.tex"
            monthly_file.write_text(
                dedent(_format_monthly_entry(year_path, month)), encoding="utf-8"
            )

    # generate the base log.tex
    generate_log(journal_path, entries)


def _parse_entries(entries_path: Path) -> Dict[str, List[str]]:
    """return a dict of {year: [month], ...} from all saved entries"""

    entries = {}

    years = [f.name for f in entries_path.iterdir() if f.is_dir()]
    years.sort()

    for year in years:
        months_folder = entries_path / year
        entries[year] = [f.name for f in months_folder.iterdir() if f.is_dir()]
        entries[year].sort()

    return entries


def _format_monthly_entry(year_path: Path, month: str) -> str:
    """return text for .tex file of accumulated monthly entries"""
    month_folder = year_path / month
    daily_entries = [f.name for f in month_folder.iterdir() if f.is_file()]
    daily_entries.sort()

    formatted_entries = [
        f"\\input{{{month_folder}/{entry.strip()}}}" for entry in daily_entries
    ]
    return "\n".join(formatted_entries)


def build_journal(journal_name: str, config: WaldenConfiguration) -> int:
    """Compile and save journal as pdf"""

    journal_name = journal_name[0]

    journal_path = config.journals[journal_name].path

    entries_path = journal_path / "entries"
    if not entries_path.exists():
        raise WaldenException("Need to have at least 1 entry before compiling journal!")

    # generate monthly tex files and log.tex
    _generate_latex_structure(journal_path)

    with set_cwd(journal_path):
        # create temp build dir
        build_dir = Path("build")
        build_dir.mkdir(exist_ok=True)

        # call pdflatex
        rc = subprocess.call(["pdflatex", "--output-directory=build", "log.tex"])
        Path("build/log.pdf").replace("log.pdf")

        # cleanup aux files
        shutil.rmtree(build_dir)

    return SUCCESS


@contextmanager
def set_cwd(path: Path):
    """context manager to allow for easy path changing"""

    cwd = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)
