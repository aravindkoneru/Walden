from pathlib import Path
from textwrap import dedent
from typing import Dict, List

MONTH_NAME = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

# path: path to root of journal
def generate_log(journal_path: Path, entries: Dict[str, List[str]]):
    headers = dedent(_initialize_header())
    document = _initialize_document(entries)

    (journal_path / "log.tex").write_text(f"{headers}\n{document}")


def _initialize_header():
    return r"""
    \documentclass[12pt]{article}
    \usepackage{graphicx}
    \usepackage{parskip}

    \setlength\evensidemargin{0.0in}
    \setlength\oddsidemargin{0.0in}
    \setlength\textwidth{6.5in}
    \setlength\textheight{9.5in}
    \setlength\topmargin{-0.5in}

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % For Footer
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \usepackage[english]{babel}
    \usepackage[utf8]{inputenc}
    \usepackage{fancyhdr}
    \usepackage{parskip}

    \pagestyle{fancy}
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    %\rhead{Share\LaTeX}
    %\lhead{Guides and tutorials}
    \rfoot{\thepage}
    \def\day{}
    \cfoot{\textit{\day}}

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % For Multiple Columns within Text
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \usepackage{multicol}

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % For Links to Websites
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \usepackage{hyperref}
    \hypersetup{
        colorlinks=true,
        linkcolor=blue,
        filecolor=magenta,
        urlcolor=cyan,
    }

    \urlstyle{same}

    """


# compile years and months into latex form
def _initialize_document(entries):
    # entries = parse_entries(f'{path}/entries')
    document = []
    document.append("\\begin{document}\n")
    document.append("\\input{aux/title}\n\\clearpage\n")

    for year in entries:
        document.append(dedent(_format_year(year)))
        for month in entries[year]:
            document.append(dedent(_format_month(year, month)))
        document.append("\\clearpage")

    document.append("\n\\end{document}\n")
    return "".join(document)


def _format_year(year):
    return f"""
    \\def\\year{{{year}}}
    \\newpage
    \\input{{aux/newyear}}
    \\newpage
    """


def _format_month(year, month):
    return f"""
    \\def\\month{{{MONTH_NAME[month]}}}
    \\newpage
    \\input{{aux/newmonth}}
    \\newpage
    \\input{{entries/{year}/{month}}}
    """
