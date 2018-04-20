import os
from . import utils

def dispatcher(isMain=False):
    page = utils.Managing.Managing(source_path_is=os.path.dirname(__file__), content_replace_keywords_with=mergeFile,
                    dump_file_name_is='dump/dump_main_projects.html', content_file_name_is='contents_projects.html',
                    script_file_name_is=__file__, base_file_name_is='base.html', data_file_is='')
    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()


def mergeFile(configurations, base_structure, contents_structure, sources_path):

        configurations['title'] = 'Sarita Adve\'s Group: Projects'
        configurations['style'] = '''
    <style type="text/css">
        .projects_page_font {
            font-family: Geneva, Arial, Helvetica, sans-serif;
        }
        .projects_page_padding {
            margin-top: -10px;
            margin-bottom: -12px;
        }
    </style>'''
        configurations['hasBody'] = True



if __name__=='__main__':
    dispatcher(True)
