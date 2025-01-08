from walden._build import _parse_entries, _generate_latex_structure
import pytest

@pytest.fixture
def _years():
    return ["2020", "2021", "2022", "2023", "2024"]

@pytest.fixture
def _months():
    return [f"{x:02}" for x in range(1,12)]

@pytest.fixture
def _days():
    return [f"{x:02}" for x in range(1, 20)]


@pytest.fixture
def test_walden_dir(tmp_path, _years, _months, _days):
    entries = tmp_path / "walden_test" / "entries"
    entries.mkdir(parents=True)

    root = entries.parents[0]

    for year in _years:
        year_dir = entries / year
        year_dir.mkdir()

        for month in _months:
            (year_dir / month).mkdir()

    yield root, _years, _months, _days

def test_parse_entries(test_walden_dir):
    root, years, months, _ = test_walden_dir
    entry_dir = root / "entries"

    entries = _parse_entries(entry_dir)

    expected = {entry_dir / year: months for year in years}
    assert entries == expected

def test_generate_latex_structure(test_walden_dir, mocker):
    root, years, months, days = test_walden_dir

    mock_generate_log = mocker.patch("walden._build.generate_log")

    _generate_latex_structure(root)
    mock_generate_log.assert_called_once()
