# How to use the scripts:
1. only update files in each projects' `Sources` folder
2. run `manage.py` with `python manage.py`
3. if necessary, individual script files and project-level `manage_main.py` files can be executed as modules

# Structure:
1. each project has a  `Sources` folder that contains
    1. `update_*.py` update each HTML page
    2. `contents_*.html` contains unique content of each HTML page
    3. `base.html` contains the base structure of all html pages in that project
    4. `manage_main.py` the project-level scripts manager
2. the top-level `Sources` folder also contains
    1. `utils/` folder that contains all classes and function definitions
    2. `publication_bibtex/` folder that contains all publications in four BibTex files `msthesis.bib`, `paper.bib`, `phdthesis.bib` and `talk.bib`
    3. `news.json` file, which contains a list of dictionaries
    4. `people.json` file, which is a dictionary of lists of dictionaries