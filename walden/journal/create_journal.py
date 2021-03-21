#!/usr/bin/env python3
import pathlib
import datetime
from pathlib import Path

from walden.utils import constants

DEFAULT_JOURNALS_PATH = constants.DEFAULT_JOURNALS_PATH


def generate_folders(journal_path):
    today = datetime.datetime.now()
    if today.month > 9:
        pathlib.Path(f'{journal_path}/entries/{today.year}/{today.month}').mkdir(parents=True)
    else:
        pathlib.Path(f'{journal_path}/entries/{today.year}/0{today.month}').mkdir(parents=True)


def gen_new_aux_page(label, is_title=False):
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


#TODO: maybe journal name can be passed in now?
def generate_resources(path, journal_name="journal"):
    files = [("newmonth.tex", "\\month"),
             ("newyear.tex", "\\year"),
             ("title.tex", journal_name)]

    Path(f"{path}/aux").mkdir()

    for file in files:
        with open(f"{path}/aux/{file[0]}", "w") as new_aux:
            new_aux.write(gen_new_aux_page(file[1], "title" in file[0]))


def init(name):
    if name is None:
        name = input('Enter desired journal name: ')

    path = f'{DEFAULT_JOURNALS_PATH}/{name}'

    while (pathlib.Path(path).exists()):
        print('Sorry, a journal with that name already exists')
        name = input('Enter desired journal name: ')
        path = f'{DEFAULT_JOURNALS_PATH}/{name}'

    pathlib.Path(path).mkdir()

    #create folder structure
    generate_resources(path, name)
    generate_folders(path)

    return (name, path)
