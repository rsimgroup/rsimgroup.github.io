import Sources
import sys

if __name__=='__main__':
    argument = Sources.utils.CommandLineHandler.CommandLineHandler().parseArguments(sys.argv)
    Sources.manage_main.dispatcher(isMain=False, specific_file=argument)
