from . import utils
import os, json

def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=mergeFile,
        dump_file_name_is='../news.html',
        content_file_name_is='contents_news.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
    )
    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()


def mergeFile(configurations, base_structure, contents_structure, sources_path):


        interface = utils.JSONUtils.JSONInterface()
        interface.load_file(target_file='news')
        news_item_list = interface.generate_news_html(interface.extract_list())

        to_replace_index = contents_structure.index('{{NEWS_ITEM}}')
        contents_structure[to_replace_index:to_replace_index+1] = news_item_list

        configurations['title'] = 'Sarita Adve\'s Group: News'
        configurations['hasBody'] = True





if __name__=='__main__':
    dispatcher(True)