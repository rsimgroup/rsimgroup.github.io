import os, json
from . import utils

import bibtexparser

def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=mergeFile,
        dump_file_name_is='dump/dump_main_pubs.html',
        content_file_name_is='contents_pubs.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
        data_file_is='publications.json'
    )

    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()

def calculatePaper(papers_list, pub_dict):

    for item in pub_dict['Papers']:
        if 'ENTRYTYPE' in item:
            papers_list.append(
                '<li class=\"style12\">' +
                '<a href=\"' +
                item['link']+
                '\" target=\"blank\">'+
                item['title']+
                '</a>, '+
                item['author']+
                ', at '+
                item['journal']+
                ', '+
                item['year']+
                '<br/>&nbsp;<br/></li>'
            )
        else:
            final_string = item['Contents']
            for key, value in item['Keyword_Link'].items():
                final_string = final_string.replace(key, '<a href=\"' + value + '\" target=\"blank\">' + key + '</a>')

            papers_list.append(
                '<li class=\"style12\">' +
                final_string +
                '&nbsp;&nbsp; '+
                '<strong>'+
                item['Display Participants']+
                '</strong> <em>' +
                item['Display Time'] +
                '</em>' +
                '<br/>&nbsp;<br/></li>'
        )

def calculatePaperBib(papers_list, bib_database):
        sorted_entries = sorted(bib_database.entries, key=lambda entry: entry['year'])
        for item in bib_database.entries:
          final_str = '<li class=\"style12\">'
          if 'url' in item.keys():
            final_str = final_str + '<a href=\"' + \
                item['url'] + \
                '\" target=\"blank\">' + \
                item['title'] + \
                '</a>, '
          else:
            final_str = final_str + \
                item['title'] + ', '
          final_str = final_str + item['author'] + \
              ', in <i>' + \
              item['booktitle'] + \
              '</i>, ' + \
              item['year'] + '.'
          if 'boldnote' in item.keys():
            final_str = final_str + " <b>" + item['boldnote'] + "</b>"
          final_str = final_str + ' <br/>&nbsp;<br/></li>'
          papers_list.append(final_str)
          
def calculateTalk(talks_list, pub_dict):
        for item in pub_dict['Talks']:
            if 'ENTRYTYPE' in item:
                talks_list.append(
                    '<li class=\"style12\">' +
                    '<a href=\"' +
                    item['link'] +
                    '\" target=\"blank\">' +
                    item['title'] +
                    '</a>, ' +
                    item['author'] +
                    ', ' +
                    item['year'] +
                    '</li>'
                )
            else:
                talk_contents = item['Contents']
                keyword_link = item['Keyword_Link']
                display_time = item['Display Time']
                display_participants = item['Display Participants']

                final_string = talk_contents
                for key, value in keyword_link.items():
                    final_string = final_string.replace(key, '<a href=\"' + value + '\" target=\"blank\">' + key + '</a>')

                talks_list.append(
                    '<li class=\"style12 pubs_margin\">' + final_string + '&nbsp;&nbsp; '+ '<strong>'+display_participants+'</strong> <em>' + display_time + '</em>' + '<br/>&nbsp;<br/></li>'
            )

def calculatePhd(phd_list, pub_dict):
    for item in pub_dict['Ph.D. Theses']:
        if 'ENTRYTYPE' in item:
            phd_list.append(
                '<li class=\"style12\">' +
                '<a href=\"' +
                item['link'] +
                '\" target=\"blank\">' +
                item['title'] +
                '</a>, ' +
                item['author'] +
                ', ' +
                item['year'] +
                '</li>'
            )
        else:
            phd_contents = item['Contents']
            keyword_link = item['Keyword_Link']
            display_time = item['Display Time']
            display_participants = item['Display Participants']

            final_string = phd_contents
            for key, value in keyword_link.items():
                final_string = final_string.replace(key, '<a href=\"' + value + '\" target=\"blank\">' + key + '</a>')

            phd_list.append(
                '<li class=\"style12 pubs_margin\">' + final_string + '&nbsp;&nbsp; ' + '<strong>' + display_participants + '</strong> <em>' + display_time + '</em>' + '<br/>&nbsp;<br/></li>'
        )

def calculateMS(ms_list, pub_dict):
    for item in pub_dict['M.S. Theses']:
        if 'ENTRYTYPE' in item:
            ms_list.append(
                '<li class=\"style12\">' +
                '<a href=\"' +
                item['link'] +
                '\" target=\"blank\">' +
                item['title'] +
                '</a>, ' +
                item['author'] +
                ', ' +
                item['year'] +
                '</li>'
            )
        else:
            ms_contents = item['Contents']
            keyword_link = item['Keyword_Link']
            display_time = item['Display Time']
            display_participants = item['Display Participants']

            final_string = ms_contents
            for key, value in keyword_link.items():
                final_string = final_string.replace(key, '<a href=\"' + value + '\" target=\"blank\">' + key + '</a>')

            ms_list.append(
                '<li class=\"style12 pubs_margin\">' + final_string + '&nbsp;&nbsp; ' + '<strong>' + display_participants + '</strong> <em>' + display_time + '</em>' + '<br/>&nbsp;<br/></li>'
        )


def mergeFile(configurations, base_structure, contents_structure, sources_path):

        with open(os.path.join(sources_path, 'publications.json'), 'r') as pub_item:
            pub_dict = json.load(pub_item)


        papers_list = []
        calculatePaper(papers_list, pub_dict)
        talks_list = []
        calculateTalk(talks_list, pub_dict)
        phd_list = []
        calculatePhd(phd_list, pub_dict)
        ms_list = []
        calculateMS(ms_list, pub_dict)

        bibfilename = os.path.join(sources_path, '../specialization/publications.bib')
        with open(bibfilename) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)

        papers_list = []
        calculatePaperBib(papers_list, bib_database)


        to_replace_index = contents_structure.index('{{PAPERS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index+1] = papers_list

        to_replace_index = contents_structure.index('{{TALKS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = talks_list

        to_replace_index = contents_structure.index('{{PHD_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = phd_list

        to_replace_index = contents_structure.index('{{MS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = ms_list


        configurations['title'] = 'Sarita Adve\'s Group: Publications'
        configurations['style'] = '''
        <style type="text/css">
        .pubs_style14_variant {
            font-weight: bold;
            text-align: right;
        }

        .pubs_style16_variant {
            font-weight: bold;
            text-align: left;
            font-size: medium;
        }

        .pubs_margin {
            margin-bottom: 12pt;
        }
        </style>
        '''
        configurations['hasBody'] = True


if __name__=='__main__':
    dispatcher(True)
