import os
import re
from . import CommandLineHandler
from . import BookKeeping


class Managing:

    def __init__(self, source_path_is, content_replace_keywords_with, dump_file_name_is, content_file_name_is, script_file_name_is, base_file_name_is='base.html', data_file_is=''):
        self._dump_file_name = dump_file_name_is
        self._data_file_name = data_file_is
        self._content_file_name = content_file_name_is
        self._script_file_name = script_file_name_is
        self._base_file_name = base_file_name_is
        self._path = source_path_is
        self._content_populator = content_replace_keywords_with
        self._book_keeping = BookKeeping.BookKeeping(time_stamp_directory_path=self.get_project_path())
        self._command_line_handler = CommandLineHandler.CommandLineHandler(self.merge_and_dump, self.get_dump_file_name())

    def get_data_file_name(self):
        return self._data_file_name

    def get_data_file_path(self):
        if self._data_file_name != '':
            return os.path.join(self._path, self._data_file_name)
        else:
            return ''

    def get_dump_file_name(self):
        return self._dump_file_name

    def get_dump_file_path(self):
        return os.path.join(self._path, self._dump_file_name)

    def get_content_file_name(self):
        return self._content_file_name

    def get_content_file_path(self):
        return os.path.join(self._path, self._content_file_name)

    def get_script_file_name(self):
        return self._script_file_name

    def get_script_file_path(self):
        return os.path.join(self._path, self._script_file_name)

    def get_base_file_name(self):
        return self._base_file_name

    def get_base_file_path(self):
        return os.path.join(self._path, self._base_file_name)

    def get_project_path(self):
        return self._path

    def execute_as_main(self, parent_manage_script_is):
        self._command_line_handler.main_exec_interface(
            parent_manage_script=parent_manage_script_is,
            book_keeping=self._book_keeping,
            dump_file_path=self.get_dump_file_path(),
            content_file_path=self.get_content_file_path(),
            script_file_path=self.get_script_file_path(),
            base_file_path=self.get_base_file_path(),
            data_file_path=self.get_data_file_path()
        )

    def execute_as_module(self):
        self._command_line_handler.sub_exec_interface(
            book_keeping=self._book_keeping,
            dump_file_path=self.get_dump_file_path(),
            content_file_path=self.get_content_file_path(),
            script_file_path=self.get_script_file_path(),
            base_file_path=self.get_base_file_path(),
            data_file_path=self.get_data_file_path()
        )

    def merge_and_dump(self):
        with open(self.get_content_file_path(), 'r') as content, open(self.get_base_file_path(), 'r') as base:
            base_structure = re.split('({{[\s\w]*}})', base.read())
            contents_structure = re.split('({{[\s\w]*}})', content.read())

            configurations = {}
            configurations['title'] = ''
            configurations['style'] = ''
            configurations['hasLeft'] = False
            configurations['hasBody'] = False
            configurations['hasRight'] = False
            configurations['left_content_left_tag'] = ''
            configurations['left_content_right_tag'] = ''
            configurations['right_content_left_tag'] = ''
            configurations['right_content_right_tag'] = ''

            self._content_populator(configurations, base_structure, contents_structure, self.get_project_path())
            self.replaceBaseWithContent(configurations, base_structure, contents_structure)
        with open(self.get_dump_file_path(), 'w') as target:
            target.write(''.join(base_structure))
            self._book_keeping.updateTimeStamp(
                dump_file_path=self.get_dump_file_path(),
                content_file_path=self.get_content_file_path(),
                script_file_path=self.get_script_file_path(),
                base_file_path=self.get_base_file_path(),
                data_file_path=self.get_data_file_path()
            )

    def replaceBaseWithContent(self, configurations, base_structure, contents_structure):


        base_structure[base_structure.index('{{PAGE_TITLE}}')] = configurations['title']
        base_structure[base_structure.index('{{STYLE}}')] = configurations['style']

        left_content_marking = base_structure.index('{{LEFT_CONTENT}}')
        if configurations['hasLeft']:
            left_content_start_idx = contents_structure.index('{{LEFT_CONTENT_START}}')
            contents_structure[left_content_start_idx] = ''
            left_content_end_idx = contents_structure.index('{{LEFT_CONTENT_END}}')
            contents_structure[left_content_end_idx] = ''
            base_structure[left_content_marking:left_content_marking + 1] = [configurations['left_content_left_tag']] + contents_structure[left_content_start_idx:left_content_end_idx + 1] + [configurations['left_content_right_tag']]
        else:
            base_structure[left_content_marking] = ''

        body_content_marking = base_structure.index('{{BODY_CONTENT}}')
        if configurations['hasBody']:
            body_content_start_idx = contents_structure.index('{{BODY_CONTENT_START}}')
            contents_structure[body_content_start_idx] = ''
            body_content_end_idx = contents_structure.index('{{BODY_CONTENT_END}}')
            contents_structure[body_content_end_idx] = ''
            base_structure[body_content_marking:body_content_marking + 1] = contents_structure[body_content_start_idx:body_content_end_idx + 1]
        else:
            base_structure[body_content_marking] = ''

        right_content_marking = base_structure.index('{{RIGHT_CONTENT}}')
        if configurations['hasRight']:
            right_content_start_idx = contents_structure.index('{{RIGHT_CONTENT_START}}')
            contents_structure[right_content_start_idx] = ''
            right_content_end_idx = contents_structure.index('{{RIGHT_CONTENT_END}}')
            contents_structure[right_content_end_idx] = ''
            base_structure[right_content_marking:right_content_marking + 1] = [configurations['right_content_left_tag']] + contents_structure[right_content_start_idx:right_content_end_idx + 1] + [configurations['right_content_right_tag']]
        else:
            base_structure[right_content_marking] = ''