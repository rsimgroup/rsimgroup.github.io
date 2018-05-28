class TextGenerator:
    def __init__(self, page_name=''):
        self.page_name = page_name

    def promptGenerator(self, parent_manage_script):
        '''
        This function returns the warning when the script is manually generated
        :param page_name: the dump file name
        :param parent_manage_script: the parent-manage script
        :return: string
        '''
        prompt = '''
        This script will only update {} page. If you want to update more pages at once, you may want to try {} or manage.py
        '''.format(self.page_name, parent_manage_script)
        return prompt

    def exitGenerator(self, isInvalid=False, isLeave=False, isFinish=False):
        '''
        This function returns the exit text
        :param page_name: string, name of the page being updated
        :param isInvalid: bool, True if this message is about invalid commandline input
        :param isLeave: bool, True if this message is shown after user chooses to leave
        :param isFinish: bool, True if this message is about normal exit
        :return: string
        '''
        if isInvalid:
            return 'Input is invalid!'
        if isLeave:
            return '~~~~~'
        if isFinish:
            return 'Finish updating {}'.format(self.page_name)
        return ''

    def transitionGenerator(self):
        return '{} is being updated!'.format(self.page_name)

    @staticmethod
    def at_least_one_sorted_error(*keys):
        '''
        This function should called when at least one key in sorting failed
        :param keys: a list of strings
        :return: None
        '''
        temp = [key for key in keys]
        temp = ' '.join(temp)
        print('At least one of '+temp+' not in object! Proceed to sorting by single key!')

    @staticmethod
    def sort_key_does_not_exist(key):
        '''
        This function should be called when the current key in sorting failed
        :param key: a string
        :return: None
        '''
        print(key + ' does not exist in the object!')

    @staticmethod
    def sort_failed():
        '''
        This function should be called when all keys failed in sorting
        :return: None
        '''
        print('Sorting failed! Proceed without sorting!')

    @staticmethod
    def time_does_not_exist():
        '''
        This function should be called when try to use 'time' to sort but in fact should use 'year'
        :return: None
        '''
        print('time attribute does not exist in the dictionary. Proceed with year attribute.')

    @staticmethod
    def file_dispatcher_prompt(file_array, project_name):
        '''
        This function should be called by file dispatcher class, used in each project-level manage_main.py
        :param file_array: a list of strings
        :param project_name: a string
        :return: a string
        '''
        return '''
        This script will try to execute following files (in project {0} ): 
            {1}
        If you want to update the entire website, you may want to try 'Manage.py'
                    '''.format(project_name, ', '.join(file_array))


    @staticmethod
    def toplevel_manage_prompt():
        '''
        This function should be called by top-level manage.py
        :return: a string
        '''
        return '''
This script will update all HTML files using their JSON or BibTex files.

This script does not accept individual file arguments.
    '''