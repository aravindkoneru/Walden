# Goal

Develop a simple automated journaling system that removes the pain points of maintenance and
organization, allowing the user to focus on writing. 

# Install

Available via pip: `pip install walden`

# Usage

Walden will create a `journals/` folder in your home directory. This is where all your output and
.tex files will be stored. The commands are:

| Flag                            | Description                         |
|---------------------------------|-------------------------------------|
| walden -h                       | show help dialog                    |
| walden -delete <journal name>   | Delete an existing journal          |
| walden -today  <journal name>   | New entry in specified journal      |
| walden -list                    | List names of journals              |
| walden -build  <journal name>   | Compile journal as .pdf             |
| walden -view   <journal name>   | View journal as .pdf (OS dependent) |


# TODO:
-  change path where journals are stored
-  allow journal import/export
-  plug-in system for things like weather/question of the day


