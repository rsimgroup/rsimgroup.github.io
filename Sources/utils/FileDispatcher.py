import os, sys
from . import CommandLineHandler
from .TextGenerator import TextGenerator as text_gen

def FileDispatcher(file_array, call_back, called_as_main=False, specific_file='', project_name=''):
    # Should be able to be called as main, when target file can either be provided when called or inputed from command line. If not called as main then requires specific file, or will update all

    if called_as_main:
        print(text_gen.file_dispatcher_prompt(project_name, file_array))
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
                print('Updating {0} now in the project {1}!'.format(argument, project_name))
                call_back(argument)
                print('{0} has been updated in the project {1}!'.format(argument, project_name))
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
            print('Updating all files now in the project {}!'.format(project_name))
            call_back()
            return

    finish = 'Finish executing this sub-manage script in project '+project_name+'! \n'
    print(finish)


