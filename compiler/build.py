#/usr/bin/env python3
import pathlib
import os
from textwrap import dedent
import subprocess
import shutil

import compiler.log_generator as log_generator

# compiles the journal using pdflatex
def compile_journal(journal_path):
    entries = parse_entries(f'{journal_path}/entries')
    compile_months(f'{journal_path}/entries', entries)
    log_generator.generate_log(journal_path, entries)

    #TODO: Make this cleaner using context managing 
    current_cwd = pathlib.Path.cwd()
    os.chdir(f'{journal_path}')

    # compile journal 
    pathlib.Path('build').mkdir(exist_ok=True)
    subprocess.call(['pdflatex', '-output-directory=build', 'log.tex'])

    #cleanup aux files
    pathlib.Path('build/log.pdf').replace('log.pdf')
    shutil.rmtree(pathlib.Path('build'))

    #TODO cleanup misc monthly files
    os.chdir(current_cwd)



# get months within a year
def parse_entries(path):
    entries = dict()

    years_folder = pathlib.Path(path)

    years = [str(f)[str(f).rindex('/')+1:] for f in years_folder.iterdir() if f.is_dir()]
    years.sort()

    for year in years:
        months_folder = pathlib.Path(f'{path}/{year}')
        entries[year] = [str(f)[str(f).rindex('/')+1:] for f in months_folder.iterdir() if f.is_dir()]
        entries[year].sort()

    return entries


def compile_months(entries_path, entries):
    for year in entries:
        for month in entries[year]:
            with open(f'{entries_path}/{year}/{month}.tex', 'w') as monthly_entry:
                monthly_entry.write(dedent(format_month(f'{entries_path}/{year}/{month}', year, month)))


def format_month(month_path, year, month):
    month_folder = pathlib.Path(month_path)
    daily_entries = [str(f)[str(f).rindex('/')+1:] for f in month_folder.iterdir() if f.is_file()]
    daily_entries.sort()

    formatted_entries = []
    for entry in daily_entries:
        formatted_entries.append(f'\\input{{entries/{year}/{month}/{entry.strip()}}}')

    return '\n'.join(formatted_entries)



if __name__ == '__main__':
    compile_journal('../journals/a')


