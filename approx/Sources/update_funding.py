import utils
import os

def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=addContents,
        dump_file_name_is='../funding.html',
        content_file_name_is='contents_funding.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
    )

    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()


def addContents(configurations, base_structure, contents_structure, sources_path):

        configurations['title'] = 'Approximate: Funding'
        configurations['hasBody'] = True



if __name__=='__main__':
    dispatcher(True)
