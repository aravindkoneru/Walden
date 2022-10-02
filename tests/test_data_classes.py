import pytest

from walden._errors import WaldenException
from walden._data_classes import JournalConfiguration, WaldenConfiguration


@pytest.fixture
def base_walden_config(tmp_path):
    cfg_path = tmp_path
    d_j_path = tmp_path / "journals"
    journals = {}

    return WaldenConfiguration(
        config_path=cfg_path, default_journal_path=d_j_path, journals=journals
    )


def test_test_journal_config(tmp_path):
    j_name = "test"
    j_path = tmp_path / "test"

    j_config = JournalConfiguration(name=j_name, path=j_path)

    assert j_config.name == j_name
    assert j_config.path == j_path

    assert j_config.to_dict() == {"path": str(j_path)}


def test_walden_config(tmp_path):
    cfg_path = tmp_path
    d_j_path = tmp_path / "journals"
    journals = {}

    w_config = WaldenConfiguration(
        config_path=cfg_path, default_journal_path=d_j_path, journals=journals
    )

    assert w_config.config_path == cfg_path
    assert w_config.default_journal_path == d_j_path
    assert w_config.journals == journals


def test_add_journal_to_config(base_walden_config, tmp_path):
    j_name = "test"
    j_path = base_walden_config.default_journal_path / "test"
    base_walden_config.add_journal(j_name, j_path)

    assert base_walden_config.get_journal(j_name) == JournalConfiguration(
        j_name, j_path
    )

    # alert raised on same name
    with pytest.raises(WaldenException):
        base_walden_config.add_journal(j_name, tmp_path / "new_path")

    j_path.mkdir(parents=True, exist_ok=False)

    # alert raised on same path
    with pytest.raises(WaldenException):
        base_walden_config.add_journal("new_name", j_path)
