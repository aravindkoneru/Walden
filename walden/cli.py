import click

from .cli_options import *

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))

@create
@view
@delete
@show_list
@today
@build
def cli(create_journal, view_journal, delete_journal, list_journals, edit_journal, build_journal):
    elif create_journal:
        #TODO: create journal
    elif view_journal:
        # TODO: view journal
    elif delete_journal:
        #TODO: delete journal
    elif list_journals:
        #TODO: list journals
    elif edit_journals:
        #TODO: edit journal
    elif build_journals:
        #TODO: build journal
