from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class JournalConfiguration:
    name: str
    path: Path

    def __str__(self):
        return f"{name} at path: {path}"


@dataclass
class WaldenConfiguration:
    config_path: Path
    default_journal_path: Path
    journals: Dict[str, JournalConfiguration]
