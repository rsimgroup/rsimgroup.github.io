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

    def exitGenerator(self, isInvalid=False, isLeave=False, isAlreadyUpdated=False, isFinish=False):
        '''
        This function returns the exit text
        :param page_name: string, name of the page being updated
        :param isInvalid: bool, True if this message is about invalid commandline input
        :param isLeave: bool, True if this message is shown after user chooses to leave
        :param isAlreadyUpdated: bool, True if this message is about no changes made
        :param isFinish: bool, True if this message is about normal exit
        :return: string
        '''
        if isInvalid:
            return 'Input is invalid!'
        if isLeave:
            return '~~~~~'
        if isFinish:
            return 'Finish updating {}'.format(self.page_name)
        if isAlreadyUpdated:
            return '{} is already up to date! No changes made!'.format(self.page_name)
        return ''

    def transitionGenerator(self):
        return '{} is being updated!'.format(self.page_name)
