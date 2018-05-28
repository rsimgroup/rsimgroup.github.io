import os, sys
from . import CommandLineHandler

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


    if called_as_main:
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


