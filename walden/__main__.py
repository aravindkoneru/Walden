import sys
import click

import walden.cli as walden

@click.command()
@click.option(
    "-i", "-init", "init"
)
#@click.option(
#    "-h", "--help", "help_arg",
#    is_flag=True
#)
@click.option("-d", "--delete", "delete")
@click.option("-l", "--list", "list_arg")
@click.option("-t", "--today", "today")
@click.option("-b", "--build", "build")
@click.option("-v", "--view", "view")
def main(init, help_arg, delete, list_arg, today, build, view):
    print(init)
    print(help_arg)
    print(delete)
    print(list_arg)
    print(today)
    print(build)
    print(view)

#def main(args=None):
#    # TODO: use arg parse instead?
#    if len(sys.argv) == 1 or sys.argv[1] == '-h':
#        walden.show_help()
#        sys.exit(0)
#    else:
#        walden.main(sys.argv[1:])


if __name__ == "__main__":
    #sys.exit(-1)
    main()
