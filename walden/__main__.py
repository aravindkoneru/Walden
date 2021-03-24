import sys


def main(args=None):
    from .cli import cli as main

    main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
