#!/usr/bin/env python
# library imports
import sys
import pathlib
import pickle
import shutil
# package imports
import compiler
import journal


DEFAULT_JOURNALS_PATH = 'journals'


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


def is_command(to_check):
    return to_check in ['-h', '-init', '-list']

    
# save journal name and path to .journals_info file
# journal_info = (name, path)
def save_journal_info(journal_info):
    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )
    meta_data[journal_info[0]] = journal_info[1]
    pickle.dump(meta_data, open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'wb'))
    return journal_info[0]


def delete_journal(journal_name):
    if journal_name is None:
        return 'No journal specified. See journal -h for help.'

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
        return f'No journal named "{journal_name}" exists. See journal -list for list of journals.'


def process_today(journal_name):
    if journal_name is None:
        print('No journal specified. See journal -h for help.')
    
    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    if journal_name in meta_data:
        journal.edit_today(meta_data[journal_name])
    else:
        print(f'No journal named "{journal_name}" exists. See journal -list for list of journals.')


def list_journals():
    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )

    journal_names = ['Journals:']
    for name in meta_data:
        journal_names.append(name)

    return '\n'.join(journal_names)


def main(args):
    check_and_create_journals_folder()

    command = args[0]
    argument = args[1] if 1 < len(args) and not is_command(args[1]) else None

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
    elif command == 'view'
        process_view(argument)
    else:
        print(f'Invalid command "{command}". Run journal -h for help.')


if __name__=='__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        show_help()
        sys.exit(0)

    else:
        main(sys.argv[1:])
