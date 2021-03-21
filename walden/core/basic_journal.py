from .base_journal import BaseJournal

class BasicJournal(BaseJournal):
    JOURNAL_TYPE = "BasicJournal"

    def __init__(self, journal_name, journal_base_path):
        super().__init__(journal_name, journal_base_path)

    def new_entry_page(self):
        """
        return the latex string to be used for new daily entries to the journal
        """
        entry = []
        today = datetime.now()

        entry.append(today.strftime("\\def\\day{\\textit{%B %d, %Y}}"))
        entry.append(today.strftime("\\def\\weekday{\\textit{%A}}"))
        entry.append("\\subsection*{\\weekday, \\day}\n\n")

        return "\n".join(entry)

    def _get_tex_pages(self):
        """
        Should return all the latex files that need to be added to aux/ for the journal.
        The expected return format is a dictionary: {filename: latex_str, ....}
        """
        files = [("newmonth.tex", "\\month"),
                 ("newyear.tex", "\\year"),
                 ("title.tex", self._journal_name)]

        return {file[0]: self._gen_aux_page(file[1], "title" in file[0]) for file in files}

    def build(self):
        """
        build the journal by running the necessary latex commands
        """
        raise NotImplementedError("build() not implemented")

    def _gen_aux_page(self, label, is_title=False):
        page = []

        if is_title:
            page.append("\\thispagestyle{empty}")

        page.append("\\begin{center}")
        page.append("\t\\vfil")
        page.append("\t\\vspace*{0.4\\textheight}\n")
        page.append("\t\\Huge")
        page.append(f"\t\\bf{{{label}}}\n")
        page.append("\t\\normalsize")
        page.append("\\end{center}")

        return "\n".join(page)
