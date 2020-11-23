#!/usr/bin/env python3
import pathlib
from textwrap import dedent

MONTH_NAME = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }

# path: path to root of journal
def generate_log(path, entries):
    headers = initialize_header()
    document = initialize_document(entries)

    with open(f'{path}/log.tex', 'w') as log:
        log.write(dedent(headers))
        log.write(document)


def initialize_header():
    return r'''
    \documentclass[12pt]{article}
    \usepackage{graphicx}

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

    '''


# compile years and months into latex form
def initialize_document(entries):
    #entries = parse_entries(f'{path}/entries')
    document = []
    document.append('\\begin{document}\n')
    document.append('\\input{aux/title}\n\\clearpage\n')

    for year in entries:
        document.append(dedent(format_year(year)))
        for month in entries[year]:
            document.append(dedent(format_month(year, month)))
        document.append('\\clearpage')

    document.append('\n\\end{document}\n')
    return ''.join(document)


def format_year(year):
    return f'''
    \\def\\year{{{year}}}
    \\input{{aux/newyear}}
    \\clearpage
    '''


def format_month(year, month):
    return f'''
    \\def\\month{{{MONTH_NAME[month]}}}
    \\input{{aux/newmonth}}
    \\clearpage
    \\input{{entries/{year}/{month}}}
    '''
