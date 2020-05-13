#!/usr/bin/env python
# library imports
import sys
import pathlib
import pickle
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
    -init <journal_name>?: create new journal
    -new_entry <journal_name>: new entry in specified journal
    -list: list names of journals
    '''
    print(message)


def is_command(to_check):
    return to_check in ['-h', '-init', '-list']

    
# save journal name and path to .journals_info file
# journal_info = (name, path)
def save_journal_info(journal_info):
    meta_data = pickle.load( open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'rb') )
    meta_data[journal_info[0]] = journal_info[1]
    print(meta_data)
    pickle.dump(meta_data, open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'wb'))
    

def main(args):
    check_and_create_journals_folder()

    for x in range (0, len(args)):
        if args[x] == '-init':
            journal_info = journal.init(args[x+1] if x+1 < len(args) and not is_command(args[x+1]) else None)
            save_journal_info(journal_info)
        elif args[x] == '-h':
            show_help()
        elif args[x] == '-list':
            print('TODO: implement list')



if __name__=='__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        show_help()
        sys.exit(0)

    else:
        main(sys.argv[1:])
