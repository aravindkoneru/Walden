#!/usr/bin/env python3
# library imports
import sys
import pathlib
import pickle
import shutil
import subprocess
import signal

# package imports
import walden.compiler as compiler
import walden.journal as journal
from walden.utils import constants


DEFAULT_JOURNALS_PATH = constants.DEFAULT_JOURNALS_PATH

def term_handler(signum, frame):
    #TODO: maybe this can be improved?
    exit(-1)

signal.signal(signal.SIGINT, term_handler)

def check_and_create_journals_folder():
    if not pathlib.Path(DEFAULT_JOURNALS_PATH).exists():
        pathlib.Path(DEFAULT_JOURNALS_PATH).mkdir()
        pickle.dump( {}, open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'wb'))


def show_help():
    message = '''
    -h: show this dialog
    init <journal_name>?: create new journal
    delete <journal_name>: delete an existing journal
    today <journal_name>: new entry in specified journal
    list: list names of journals
    build <journal_name>: compile journal into .pdf
    view <journal_name>: view journal as .pdf
    '''
    print(message)



# save journal name and path to .journals_info file
# journal_info = (name, path)
def save_journal_info(journal_info):
    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )
    meta_data[journal_info[0]] = journal_info[1]
    pickle.dump(meta_data, open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'wb'))
    return journal_info[0]


def delete_journal(journal_name):
    if journal_name is None:
        return 'No journal specified. See walden -h for help.'

    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    if journal_name in meta_data:
        confirmation = ''
        while not (confirmation.lower() == 'y' or confirmation.lower() == 'n'):
            confirmation = input(f'Are you sure you want to delete "{journal_name}"? (Y/N): ')

        if confirmation.casefold() == 'y'.casefold():
            path = pathlib.Path(meta_data.pop(journal_name))
            pickle.dump(meta_data, open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'wb'))
            shutil.rmtree(path)
            return f'journal "{journal_name}" deleted.'
        else:
            return f'"{journal_name}" not deleted.'

    else:
        return f'No journal named "{journal_name}" exists. See walden -list for list of journals.'


def process_today(journal_name):
    if journal_name is None:
        print('No journal specified. See walden -h for help.')
        return

    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    if journal_name in meta_data:
        journal.edit_today(meta_data[journal_name])
    else:
        print(f'No journal named "{journal_name}" exists. See walden -list for list of journals.')


def list_journals():
    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    journal_names = ['Journals:']
    for name in meta_data:
        journal_names.append(name)

    return '\n'.join(journal_names)


def process_build(journal_name):
    if journal_name is None:
        print('No journal specified. See walden -h for help.')
        return

    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    if journal_name in meta_data:
        compiler.compile_journal(meta_data[journal_name])
    else:
        print(f'No journal named "{journal_name}" exists. See walden -list for list of journals.')


def process_view(journal_name):
    if journal_name is None:
        print('No journal specified. See walden -h for help.')
        return

    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    if journal_name in meta_data:
        if not pathlib.Path(f'{meta_data[journal_name]}/log.pdf').exists():
            compiler.compile_journal(meta_data[journal_name])
        subprocess.call(['open', f'{meta_data[journal_name]}/log.pdf'])
    else:
        print(f'No journal named "{journal_name}" exists. See walden -list for list of journals.')

#TODO: allow changing path where journals are stored
#def process_set_path(new_journal_path):
#    if new_journal_path is None:
#        print(f'No new journal path specified. See walden -h for help.')
#
#    new_journal_path = 



def main(args):
    check_and_create_journals_folder()

    command = args[0]
    argument = args[1] if 1 < len(args) else None

    if command == 'init':
        journal_info = journal.init(argument)
        journal_name = save_journal_info(journal_info)
        print(f'{journal_name} created!')
    elif command == '-h':
        show_help()
    elif command == 'delete':
        response = delete_journal(argument)
        print(response)
    elif command == 'list':
        names = list_journals()
        print(names)
    elif command == 'today':
        res = process_today(argument)
    elif command == 'build':
        process_build(argument)
    elif command == 'view':
        process_view(argument)
    #elif command == 'set-path':
    #    process_set_path(argument)
    else:
        print(f'Invalid command "{command}". See walden -h for help.')
