import yaml
from pathlib import Path

from .constants import PICKLE_NAME


def ensure_config(func):
    def check(*args):
        if not _exists():
            _create()
        return func(*args)

    return check


def _create():
    try:
        with open(Path.home() / PICKLE_NAME, "w") as config_file:
            yaml.dump({}, config_file)

        return True
    except Exception as e:
        print(f"Caught {e}")
        return False


def _exists():
    return Path(Path.home() / PICKLE_NAME).exists()


def _write_to_yaml(journal_info):
    try:
        with open(Path.home() / PICKLE_NAME, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)

        config[journal_info["name"]] = journal_info

        with open(Path.home() / PICKLE_NAME, "w") as config_file:
            yaml.dump(config, config_file)

        return True
    except Exception as e:
        raise e
        return False


@ensure_config
def save_journal_metadata(journal_info):
    return _write_to_yaml(journal_info)


@ensure_config
def get_journal_info(journal_name):
    with open(Path.home() / PICKLE_NAME, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config.get(journal_name, None)


@ensure_config
def get_journal_list():
    with open(Path.home() / PICKLE_NAME, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config.keys()
