from abc import ABCMeta, abstractmethod
from pathlib import Path
from datetime import datetime
import shutil

from walden.utils import sanitize_journal_name

class BaseJournal(metaclass=ABCMeta):
    def __init__(self, journal_name, journal_base_path):
        self._journal_name = journal_name
        self._sanitized_name = sanitize_journal_name(journal_name)
        self._journal_path = Path(f"{journal_base_path}/{self._sanitized_name}")

    @property
    @abstractmethod
    def JOURNAL_TYPE(self):
        raise NotImplementedError("JOURNAL_TYPE not set")

    def exists(self):
        """
        check if the journal path already exists
        """
        return Path(self._journal_path).exists()

    def create(self):
        """
        create the necessary folder structure and latex templates necessary
        for the journal
        """

        try:
            # create the top level folder for the journal
            self._journal_path.mkdir(parents=True)

            # create the folders to hold the entries
            today = datetime.now()
            year = today.year
            month = today.strftime("%m")
            day = today.strftime("%d")
            Path(f"{self._journal_path}/entries/{year}/{month}/{day}").mkdir(parents=True)

            # add .tex resources for the journal
            Path(f"{self._journal_path}/aux").mkdir()
            tex_pages = self._get_tex_pages()

            for f_name in tex_pages:
                with open(f"{self._journal_path}/aux/{f_name}", "w") as new_page:
                    new_page.write(tex_pages[f_name])

            return True
        except Exception as e:
            #print(f"Caught: {e}")
            self.delete()
            return False

    def delete(self):
        if self.exists():
            shutil.rmtree(self._journal_path)

    def get_metadata(self):
        return {
            "type": self.JOURNAL_TYPE,
            "name": self._journal_name,
            "path": str(self._journal_path)
        }


    @abstractmethod
    def new_entry_page(self):
        """
        return the latex string to be used for new daily entries to the journal
        """
        raise NotImplementedError("new_entry_page() not implemented")

    @abstractmethod
    def _get_tex_pages(self):
        """
        Should return all the latex files that need to be added to aux/ for the journal.
        The expected return format is a dictionary: {filename: latex_str, ....}
        """
        raise NotImplementedError("_get_tex_pages() not implemented")

    @abstractmethod
    def build(self):
        """
        build the journal by running the necessary latex commands
        """
        raise NotImplementedError("build() not implemented")
