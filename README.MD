# Use The Scripts:

* #### If you simply want to add new entries to Publication from Bibtex: 
    * Place the entire Bibtex into **interface.bib**. You can put multiple entries separated by carriage return. Right now only papers types including 'article', 'phdthesis' and 'mastersthesis' are supported
    * Manually run **manage.py** without any arguments: `python3 manage.py`
   
* #### If you want to update People, News, Softwares and Publications from other sources:
    * Unfortunately you have to open each json file, including people.json, news.json and publications.json, located in _Sources_ folder. Don't worry about syntax and just copy-paste existing entries (and of course modify the contents). Don't forget to add a comma after the newly added entry. Entries at the top will be correspondingly placed at the top of HTML files
    * You do not have to do anything else

* #### If you want to modify existing HTML contents apart from simply adding new entries:
    * You have to open each HTML file in _Sources_ folder.
    * HTML files with prefix 'contents_' are contents unique to each page
    * HTML file with name 'base' contains the structure that is universal to all pages belonged to this sub-application
    * Python scripts with prefix 'update' are used to only update 'contents' HTML files
    * Python scripts inside _utils_ are classes definitions
    * HTML files in _dump_ serve as caches to avoid unnecessary re-rendering
    * If you did not create a new file, you do not need to invoke any script for it to take effects. If you created a new file, then you must modify the manage_main.py file and add new entries.

* #### More options:
    * Only following files are supposed to be executed as a script, meaning that you may use `python3 file_name.py` to execute them:
        * **manage.py**:
            This file should be the only interface to you.
        * **redirect.py**:
            This file is intended for page rendering. Do not need to modify or invoke it.
    * All files in _Sources_ folders are modules. They can be executed with the command `python3 -m file_name` (WITHOUT .py !!!). 
    * All script files with .py (except for those in _utils_) can be invoked with flag -update. The functionality is the same except that there will not be prompts for you to enter anything