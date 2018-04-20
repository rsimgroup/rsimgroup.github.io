import os, sys, json
from . import CommandLineHandler



def updatePub(bib_path, pub_path):
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'library/bibtex'))
    import bibtexparser

    if os.stat(os.path.join(bib_path, 'interface.bib')).st_size == 0:
        return False

    with open(os.path.join(pub_path, 'publications.json'), 'r') as pub_file, open(
            os.path.join(bib_path, 'interface.bib'), 'r') as bib_file:
        pub = json.load(pub_file)
        bib = bibtexparser.load(bib_file)

        for dict in bib.entries:
            type = dict['ENTRYTYPE']
            if type == 'mastersthesis':
                pub['M.S. Theses'] = [dict] + pub['M.S. Theses']
            elif type == 'phdthesis':
                pub['Ph.D. Theses'] = [dict] + pub['Ph.D. Theses']
            else:
                pub['Papers'] = [dict] + pub['Papers']
    with open(os.path.join(pub_path, 'publications.json'), 'w') as pub_file, open(
            os.path.join(bib_path, 'interface.bib'), 'w') as bib_file:
        json.dump(pub, pub_file)

    return True


def FileDispatcher(file_array, call_back, called_as_main=False, specific_file=''):
    # Should be able to be called as main, when target file can either be provided when called or inputed from command line. If not called as main then requires specific file, or will update all
    if called_as_main:
        prompt = '''
This script will first check whether interface.bib file has changed and try to update it. If the bibtex file is not empty, then it will clear the file after merging it with publications

Then it will try to execute following files: 
    {}
If you want to update the entire website, you may want to try 'Manage.py'
            '''.format(', '.join(file_array))
        print(prompt)

    bib_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = updatePub(bib_path=bib_path, pub_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


    if called_as_main:
        if result:
            prompt = '''
Bibtex file has been cleared and already merged with publication database.
            '''
            print(prompt)
        else:
            prompt = '''
Bibtex file is empty.
            '''
            print(prompt)

        if specific_file == '':
            argument = CommandLineHandler.CommandLineHandler().parseArguments(argv=sys.argv)
            if argument == 'none':
                answer = input('Continue to update all files? y/n \n')
                if answer != 'y':
                    print('Okay. Exit now!')
                    return
                else:
                    call_back()
            elif argument != 'all' and argument in file_array:
                print('Updating {} now!'.format(argument))
                call_back(argument)
                print('{} has been updated!'.format(argument))
            elif argument == 'all':
                call_back()
            else:
                print('Okay. Exit now!')
                return
        elif specific_file in file_array:
            print('Updating {} now!'.format(specific_file))
            call_back(specific_file)
            print('{} has been updated!'.format(specific_file))
        else:
            print('No target file provided. Exit now.')
            return

    else:
        if specific_file in file_array:
            call_back(specific_file)
        else:
            print('Updating all files now!')
            call_back()
            return

    finish = 'Finish executing this sub-manage script!'
    print(finish)


