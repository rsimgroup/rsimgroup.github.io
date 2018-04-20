import sys
import Sources.utils.CommandLineHandler
import Sources.manage_main

if __name__=='__main__':
    prompt = '''
This script will update all HTML and json files if they have been modified or need to be modified (i.e. interface.bib is not empty meaning that publication.json needs to be updated).

This script does not accept individual file arguments.
    '''
    print(prompt)
    argument = Sources.utils.CommandLineHandler.CommandLineHandler().parseArguments(sys.argv)
    if argument == 'all':
        Sources.manage_main.dispatcher()
    else:
        yes = input('Continue to update all files? y/n \n')
        if yes == 'y':
            print('Updating now! \n \n')
            Sources.manage_main.dispatcher()
            print('Finish executing main script!')
        else:
            print('Exiting main script!')
