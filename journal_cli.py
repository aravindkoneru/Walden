#!/usr/bin/env python
import sys
import pathlib
import datetime
import shutil
import compiler


DEFAULT_JOURNALS_PATH = 'journals'


def check_and_create_journals_folder():
    if not pathlib.Path(DEFAULT_JOURNALS_PATH).exists():
        pathlib.Path(DEFAULT_JOURNALS_PATH).mkdir()
        
        meta_data = open(f'{DEFAULT_JOURNALS_PATH}/.journals_info', 'w')
        meta_data.write('')
        meta_data.close()


def show_help():
    message = '''
    -h: show this dialog
    -init <path>: create new journal.mkdir()
    -list: list names of journals
    '''
    print(message)


def is_command(to_check):
    return to_check in ['-h', '-init', '-list']


def generate_folders(journal_path):
    today = datetime.datetime.now()
    if today.month > 9:
        pathlib.Path(f'{journal_path}/years/{today.year}/{today.month}').mkdir(parents=True)
    else:
        pathlib.Path(f'{journal_path}/years/{today.year}/0{today.month}').mkdir(parents=True)


def move_resources(path):
    shutil.copytree('resources/aux', f'{path}/aux')
    shutil.copy('resources/Makefile_template', f'{path}/Makefile')
    #shutil.copy('resources/compile_months.sh', f'{path}/aux/compile_months.sh')
    #shutil.copy('resources/log.tex', f'{path}/log.tex')
    

#def generate_makefile(journal_path):
    


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
    compiler.generate_log(path)
    #generate_makefile(path)
    


def main(args):
    check_and_create_journals_folder()

    for x in range (0, len(args)):
        if args[x] == '-init':
            init(args[x+1] if x+1 < len(args) and not is_command(args[x+1]) else None)
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
