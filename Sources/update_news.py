from . import utils
import os, json

def dispatcher(isMain=False):
    page = utils.Managing.Managing(source_path_is=os.path.dirname(__file__), content_replace_keywords_with=mergeFile,
                    dump_file_name_is='dump/dump_main_news.html', content_file_name_is='contents_news.html',
                    script_file_name_is=__file__, base_file_name_is='base.html', data_file_is='news.json')
    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()


def mergeFile(configurations, base_structure, contents_structure, sources_path):

        with open(os.path.join(sources_path, 'news.json'), 'r') as news_item:
            news_list = json.load(news_item)

        news_item_list = []
        for item in news_list:
            news_content = item['Contents']
            news_time = item['Display Time']
            news_final_string = news_content
            for key, value in item['Keyword_Link'].items():
                news_final_string = news_final_string.replace(key, '<a href=\"'+value+'\" target=\"blank\">'+key+'</a>')
            news_item_list.append('<li><p class=\"style12\">'+news_final_string+'&nbsp;&nbsp; <em>'+news_time+'</em>'+'</p></li>')

        to_replace_index = contents_structure.index('{{NEWS_ITEM}}')
        contents_structure[to_replace_index:to_replace_index+1] = news_item_list

        configurations['title'] = 'Sarita Adve\'s Group: News'
        configurations['hasBody'] = True





if __name__=='__main__':
    dispatcher(True)