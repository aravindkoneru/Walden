import pytest
from unittest.mock import patch

from .support import good_config, create_journal_fs

from walden.api._access_api import WaldenAPI
from walden._errors import WaldenException
from walden._data_classes import JournalConfiguration

API_PATH = "walden.api._access_api"


def test_lookup_journal(tmp_path):
    j_name = "random_name"
    j_path = "path"
    walden_api = WaldenAPI(config=good_config(tmp_path, {j_name: j_path}))

    journal = walden_api.get_journal_info(j_name)
    assert journal.name == j_name


def test_lookup_journal_failure(tmp_path):
    j_name = "random_name"
    j_path = "path"
    walden_api = WaldenAPI(config=good_config(tmp_path, {"other_journal": j_path}))

    with pytest.raises(WaldenException):
        journal = walden_api.get_journal_info(j_name)


def test_get_journal_entries(tmp_path):
    j_name = "test"
    j_path = tmp_path / j_name
    j_cfg = JournalConfiguration(j_name, j_path)

    create_journal_fs(j_path)

    walden_api = WaldenAPI(config=good_config(tmp_path, {j_name: j_path}))

    years = [f"202{x}" for x in range(0, 9)]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    entries = [f"{x}.tex" for x in range(10, 15)]

    assert sorted(walden_api.get_journal_entries(j_cfg)) == sorted(years)
    assert sorted(walden_api.get_journal_entries(j_cfg, year="2021")) == sorted(months)
    assert sorted(
        walden_api.get_journal_entries(j_cfg, year="2021", month="10")
    ) == sorted(entries)

    with pytest.raises(WaldenException):
        walden_api.get_journal_entries(j_cfg, year="2045")

    with pytest.raises(WaldenException):
        walden_api.get_journal_entries(j_cfg, year="2021", month="15")
