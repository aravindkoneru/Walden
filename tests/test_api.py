import pytest
from unittest.mock import patch

from .support import good_config

from walden.api._access_api import WaldenAPI
from walden._errors import WaldenException

API_PATH = "walden.api._access_api"

def test_lookup_journal(tmpdir):
    j_name = "random_name"
    j_path = "path"
    walden_api = WaldenAPI(config=good_config(tmpdir, {j_name: j_path}))

    journal = walden_api.get_journal_info(j_name)
    assert journal.name == j_name

def test_lookup_journal_failure(tmpdir):
    j_name = "random_name"
    j_path = "path"
    walden_api = WaldenAPI(config=good_config(tmpdir, {"other_journal": j_path}))

    with pytest.raises(WaldenException):
        journal = walden_api.get_journal_info(j_name)

