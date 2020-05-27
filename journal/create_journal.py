#!/usr/bin/env python3
import pathlib
import datetime
import shutil

from utils import constants

DEFAULT_JOURNALS_PATH = constants.DEFAULT_JOURNALS_PATH


def generate_folders(journal_path):
    today = datetime.datetime.now()
    if today.month > 9:
        pathlib.Path(f'{journal_path}/entries/{today.year}/{today.month}').mkdir(parents=True)
    else:
        pathlib.Path(f'{journal_path}/entries/{today.year}/0{today.month}').mkdir(parents=True)


def move_resources(path):
    shutil.copytree('resources/aux', f'{path}/aux')


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
    move_resources(path)
    generate_folders(path)

    return (name, path)
