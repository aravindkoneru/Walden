import sys
#import argparse

import walden.cli as walden

#parser = argparse.ArgumentParser(description="edit and manage your walden journals")
#parser.add_argument("init", type=str, nargs=1, help="create a new journal")
##parser.add_argument("today", type=str, nargs=1, help="edit today's entry for specified journal")
##parser.add_argument("delete", type=str, nargs=1, help="delete specified journal")
##parser.add_argument("list", type=str, nargs=1, help="list all journals managed by walden")
##parser.add_argument("build", type=str,nargs=1, help="compile the specified journal")
##parser.add_argument("view", type=str, nargs=1, help="open the specified journal (os dependent)")
#
#parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
#
#def main(args=None):
#    args = parser.parse_args()
#    print(args)


def main(args=None):
    # TODO: use arg parse instead?
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        walden.show_help()
        sys.exit(0)
    else:
        walden.main(sys.argv[1:])


#if __name__ == "__main__":
#    sys.exit(-1)
