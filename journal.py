#!/usr/bin/env python

import os
import sys
import datetime

DEFAULT_JOURNAL_PATH = 'journals'


def check_journal_exists():
    if not os.path.exists(DEFAULT_JOURNAL_PATH):
        os.mkdir(DEFAULT_JOURNAL_PATH)
        
        meta_data = open(f"{DEFAULT_JOURNAL_PATH}/.journals_info", "w")
        meta_data.write("")
        meta_data.close()


def show_help():
    message = """
    -h: show this dialog
    -init <path>: create new journal
    -list: list names of journals
    """
    print(message)


def init(path):
    # sanity check to ensure journals/ folder exists

    name = input("Enter desired journal name: ")

    
    if path is None or not os.path.exists(path):
        path = input("Enter desired path: ")

   


def main(args):
    check_journal_exists()

    for x in range (0, len(args)):
        if args[x] == '-init':
            init(args[x+1] if x+1 < len(args) else None)

    print(args)


if __name__=="__main__":
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        show_help()
        sys.exit(0)

    else:
        main(sys.argv[1:])
