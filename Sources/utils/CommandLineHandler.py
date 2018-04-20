from sys import argv
from . import TextGenerator

class CommandLineHandler:
    def __init__(self, function=None, dump_file_name=''):
        '''
        Initialize CommandLineHandler
        :param function: function type. Next function to execute if continue
        '''
        self.next_function = function
        self.prompt_generator = TextGenerator.TextGenerator(dump_file_name)

    def parseArguments(self, argv):
        '''
        This function parse the command line arguments to python scripts. Currently it only supports one argument, namely '-update'
        :param argv: list, the argument array
        :return: True if argument is update all
        '''
        try:
            if argv[1] == '-update' or argv[1] == '-a' or argv[1] == '-all':
                return 'all'
            else:
                return argv[1]
        except IndexError:
            return 'none'

    def main_exec_interface(self, parent_manage_script, book_keeping, dump_file_path, base_file_path, content_file_path, script_file_path, data_file_path=''):
        prompt = self.prompt_generator.promptGenerator(parent_manage_script)
        print(prompt)

        if self.parseArguments(argv) == 'all':
            choice = input('Continue? y/n \n')
        else:
            choice = 'y'

        if choice == 'n':
            print(self.prompt_generator.exitGenerator(isLeave=True))
        elif choice == 'y':
            print(self.prompt_generator.transitionGenerator())
            if not book_keeping.isModified(dump_file_path=dump_file_path, content_file_path=content_file_path, base_file_path=base_file_path, script_file_path=script_file_path, data_file_path=data_file_path):
                print(self.prompt_generator.exitGenerator(isAlreadyUpdated=True))
            else:
                self.next_function()
                print(self.prompt_generator.exitGenerator(isFinish=True))
        else:
            print(self.prompt_generator.exitGenerator(isInvalid=True))


    def sub_exec_interface(self, book_keeping, dump_file_path, base_file_path, content_file_path, script_file_path, data_file_path=''):
        if not book_keeping.isModified(dump_file_path=dump_file_path, content_file_path=content_file_path, base_file_path=base_file_path, script_file_path=script_file_path, data_file_path=data_file_path):
            print(self.prompt_generator.exitGenerator(isAlreadyUpdated=True))
        else:
            self.next_function()
            print(self.prompt_generator.exitGenerator(isFinish=True))