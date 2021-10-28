from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import toml


@dataclass
class JournalConfiguration:
    """Used to represent configuration for a journal"""

    name: str
    path: Path

    def __str__(self) -> str:
        return f"{self.name} at path: {self.path}"

    def to_dict(self) -> dict:
        """Convert class to dict representation for saving to disk as toml"""
        return {"path": str(self.path)}


@dataclass
class WaldenConfiguration:
    """Used to represent configuration file for walden"""

    config_path: Path
    default_journal_path: Path
    journals: Dict[str, JournalConfiguration]

    def save(self):
        """Write current configuration to disk"""

        config = {
            journal_name: journal_info.to_dict()
            for journal_name, journal_info in self.journals.items()
        }

        config["config_path"] = str(self.config_path)
        config["default_journal_path"] = str(self.default_journal_path)

        self.config_path.write_text(toml.dumps({"walden": config}))
