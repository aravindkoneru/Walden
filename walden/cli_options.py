import click

create = click.option(
    "-c",
    "--create",
    "create_journal",
    type=str,
    help="create a new journal",
    metavar="<journal_name>"
)

view = click.option(
    "-v",
    "--view",
    "view_journal",
    type=str,
    help="view an existing journal",
    metavar="<journal_name>"
)

delete = click.option(
    "-d",
    "--delete",
    "delete_journal",
    type=str,
    help="delete an existing journal",
    metavar="<journal_name>"
)

show_list = click.option(
    "-l",
    "--list",
    "list_journals",
    help="show a list of all journal names",
    metavar=""
)

today = click.option(
    "-t",
    "--today",
    "edit_journal",
    type=str,
    help="edit today's entry in the specified journal",
    metavar="<journal_name>"
)

build = click.option(
    "-b",
    "--build",
    "build_journal",
    type=str,
    help="build the specified journal",
    metavar="<journal_name>"
)
