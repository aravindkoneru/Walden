import pytest

from walden._list import list_journals

from .support import good_config


def test_no_journals(capsys, tmpdir):
    config = good_config(tmpdir)

    list_journals(config)

    captured = capsys.readouterr()
    assert "No journals exist yet" in captured.out


def test_journals(capsys, tmpdir):
    config = good_config(tmpdir, {"random_name": "path"})

    list_journals(config)

    captured = capsys.readouterr()
    assert "List of journals: " in captured.out
    assert "random_name" in captured.out
