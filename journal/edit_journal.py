#!/usr/bin/env python3
import pathlib
import datetime
import subprocess
import os

EDITOR = os.environ.get('EDITOR', 'vim')

def edit_today(journal_path):
    today = datetime.datetime.now()
    entry_path = None

    if today.month > 9:
        entry_path = pathlib.Path(f'{journal_path}/entries/{today.year}/{today.month}/{today.day}.tex')
    else:
        entry_path = pathlib.Path(f'{journal_path}/entries/{today.year}/0{today.month}/{today.day}.tex')

    if not entry_path.is_file():
        create_entry(entry_path)

    subprocess.call([EDITOR, entry_path])


def create_entry(entry_path):
    entry = []
    today = datetime.date.today()

    print('Creating today\'s journal entry...')

    entry.append(today.strftime("\\def\\day{\\textit{%B %d, %Y}}"))
    entry.append(today.strftime("\\def\\weekday{\\textit{%A}}"))
    entry.append("\\subsection*{\\weekday, \\day}\n\n")

    with open(entry_path, "w") as new_entry:
        new_entry.write('\n'.join(entry))


if __name__ == '__main__':
    edit_today('journals/a')
