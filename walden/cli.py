import click

from .cli_options import *
from .core import create_new_journal


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@create
@view
@delete
@show_list
@today
@build
def cli(
    create_journal: str,
    view_journal: str,
    delete_journal: str,
    list_journals: str,
    edit_journal: str,
    build_journal: str,
):
    if create_journal:
        create_new_journal(create_journal)
        # TODO: create journal
    elif view_journal:
        pass
        # TODO: view journal
    elif delete_journal:
        pass
        # TODO: delete journal
    elif list_journals:
        pass
        # TODO: list journals
    elif edit_journal:
        edit_journal_entry(edit_journal)
        pass
        # TODO: edit journal
    elif build_journal:
        pass
        # TODO: build journal
