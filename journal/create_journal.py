#!/usr/bin/env python
import pathlib
import datetime
import shutil

DEFAULT_JOURNALS_PATH = 'journals'


def generate_folders(journal_path):
    today = datetime.datetime.now()
    if today.month > 9:
        pathlib.Path(f'{journal_path}/years/{today.year}/{today.month}').mkdir(parents=True)
    else:
        pathlib.Path(f'{journal_path}/years/{today.year}/0{today.month}').mkdir(parents=True)


def move_resources(path):
    shutil.copytree('resources/aux', f'{path}/aux')
    shutil.copy('resources/Makefile_template', f'{path}/Makefile')


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
