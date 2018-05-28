from . import utils
import os


def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=addContents,
        dump_file_name_is='../index.html',
        content_file_name_is='contents_index.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
    )

    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()

def addContents(configurations, base_structure, contents_structure, sources_path):

        interface = utils.JSONUtils.JSONInterface()
        interface.load_file(target_file='news')

        limited_counter = 20
        news_item_list = interface.generate_news_html(interface.extract_list())[:limited_counter]


        to_replace_index = contents_structure.index('{{NEWS_ITEM}}')
        contents_structure[to_replace_index:to_replace_index+1] = news_item_list

        configurations['title'] = 'Sarita Adve&#39;s Group'
        configurations['hasLeft'] = True
        configurations['hasBody'] = True
        configurations['left_content_left_tag'] = '<td class="left_content" style="font-size: small; width: 275px;">'
        configurations['left_content_right_tag'] = '</td>'




if __name__=='__main__':
    dispatcher(True)
