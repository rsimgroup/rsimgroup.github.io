import os
from Sources import utils

def dispatcher(isMain=False):
    utils.Managing.ManageWrapper(
        add_content_from_function=addContents,
        script_file_name_is=__file__,
        isMain=isMain
    )


def addContents(configurations, base_structure, contents_structure, sources_path):

        interface = utils.BibtexUtils.BibtexInterface()

        papers_list = interface.generate_paper_html(interface.extract_paper_list(project='specialization'))
        talks_list = interface.generate_talk_html(interface.extract_talk_list(project='specialization'))
        phd_list = interface.generate_phdthesis_html(interface.extract_phdthesis_list(project='specialization'))

        to_replace_index = contents_structure.index('{{PAPERS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index+1] = papers_list

        to_replace_index = contents_structure.index('{{TALKS_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = talks_list

        to_replace_index = contents_structure.index('{{PHD_CONTENT}}')
        contents_structure[to_replace_index:to_replace_index + 1] = phd_list

        configurations['title'] = 'Specialization: Publications'
        configurations['style'] = """
        <style type="text/css">
        .pubs_back_to_top {
            font-weight: bold;
            text-align: right;
        }
        .pubs_margin {
            margin-bottom: 12pt;
        }
        </style>
        """
        configurations['hasBody'] = True


if __name__=='__main__':
    dispatcher(True)