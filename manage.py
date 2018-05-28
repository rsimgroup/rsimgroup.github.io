import sys
import Sources.utils
import Sources.manage_main
import approx.Sources.manage_main
import specialization.Sources.manage_main
import Sources.utils.TextGenerator

if __name__=='__main__':
    print(Sources.utils.TextGenerator.TextGenerator.toplevel_manage_prompt())
    argument = Sources.utils.CommandLineHandler.CommandLineHandler().parseArguments(sys.argv)
    if argument == 'all':
        Sources.manage_main.dispatcher()
        approx.Sources.manage_main.dispatcher()
        specialization.Sources.manage_main.dispatcher()
    else:
        yes = input('Continue to update all files? y/n \n')
        if yes == 'y':
            print('Updating now! \n \n')
            Sources.manage_main.dispatcher()
            approx.Sources.manage_main.dispatcher()
            specialization.Sources.manage_main.dispatcher()
            print('Finish executing main script!')
        else:
            print('Exiting main script!')
