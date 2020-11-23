import sys

import walden.cli as walden

def main(args=None):
    # TODO: use arg parse instead?
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        walden.show_help()
        sys.exit(0)
    else:
        walden.main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(-1)
