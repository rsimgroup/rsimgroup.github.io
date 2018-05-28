import os
import utils

def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=addContents,
        dump_file_name_is='../pubs.html',
        content_file_name_is='contents_pubs.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
    )

    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()


def addContents(configurations, base_structure, contents_structure, sources_path):

        application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        interface = utils.BibtexUtils.BibtexInterface(
            paper_path=os.path.join(application_path, 'Sources/publication_bibtex/paper.bib'),
            talk_path=os.path.join(application_path, 'Sources/publication_bibtex/talk.bib'),
            msthesis_path=os.path.join(application_path, 'Sources/publication_bibtex/msthesis.bib'),
            phdthesis_path=os.path.join(application_path, 'Sources/publication_bibtex/phdthesis.bib')
        )

        papers_list = interface.generate_paper_html(interface.extract_paper_list(project='approx'))
        talks_list = interface.generate_talk_html(interface.extract_talk_list(project='approx'))
        phd_list = interface.generate_phdthesis_html(interface.extract_phdthesis_list(project='approx'))


        to_replace_index = contents_structure.index('{{PAPERS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index+1] = papers_list

        to_replace_index = contents_structure.index('{{TALKS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = talks_list

        to_replace_index = contents_structure.index('{{PHD_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = phd_list


        configurations['title'] = 'Approximation: Publications'
        configurations['style'] = '''
        <style type="text/css">
        .pubs_back_to_top {
            font-weight: bold;
            text-align: right;
        }
        .pubs_margin {
            margin-bottom: 12pt;
        }
        </style>
        '''
        configurations['hasBody'] = True


if __name__=='__main__':
    dispatcher(True)