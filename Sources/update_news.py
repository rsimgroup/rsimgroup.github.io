from . import utils
import os, json


def dispatcher(isMain=False):
    utils.Managing.ManageWrapper(
        add_content_from_function=addContents,
        script_file_name_is=__file__,
        isMain=isMain
    )


def addContents(configurations, base_structure, contents_structure, sources_path):

        interface = utils.JSONUtils.JSONInterface(file_path='news.json', target='news')
        news_item_list = interface.generate_news_html(interface.extract_list())

        to_replace_index = contents_structure.index('{{NEWS_ITEM}}')
        contents_structure[to_replace_index:to_replace_index+1] = news_item_list

        configurations['title'] = 'Sarita Adve\'s Group: News'
        configurations['hasBody'] = True





if __name__=='__main__':
    dispatcher(True)