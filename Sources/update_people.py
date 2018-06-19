from . import utils
import os

def dispatcher(isMain=False):
    utils.Managing.ManageWrapper(
        add_content_from_function=addContents,
        script_file_name_is=__file__,
        isMain=isMain
    )



def addContents(configurations, base_structure, contents_structure, sources_path):

        interface = utils.JSONUtils.JSONInterface(file_path='people.json', target='people')

        style = """
        <style type="text/css">
            .align_text_right {
                text-align: right;
            }
            .paragraph_margin {
              margin-left: 0.5in;
            }
            .entry_width {
              width: 25%;
            }
        </style>
        """

        title = 'Sarita Adve\'s Group: People'

        faculty_list = interface.generate_faculty_html(interface.extract_list(type='Faculty'))

        curr_grad_list = interface.generate_current_graduate_html(interface.extract_list(type='Current graduate students'))

        curr_collab_list = interface.generate_current_collaborator_html(interface.extract_list(type='Current collaborators'))

        prev_phd_list = interface.generate_graduated_phd_html(interface.extract_list(type='Graduated Ph.D. students'))

        prev_ms_list = interface.generate_graduated_ms_html(interface.extract_list(type='Graduated M.S. students'))

        prev_ug_list = interface.generate_graduated_ug_html(interface.extract_list(type='Past visiting students and undergraduate students'))

        to_replace_index = contents_structure.index('{{FACULTY_ITEM}}')
        contents_structure[to_replace_index:to_replace_index+1] = faculty_list

        to_replace_index = contents_structure.index('{{CURR_GRAD_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = curr_grad_list

        to_replace_index = contents_structure.index('{{CURR_COLLAB_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = curr_collab_list

        to_replace_index = contents_structure.index('{{PREV_PHD_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = prev_phd_list

        to_replace_index = contents_structure.index('{{PREV_GRAD_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = prev_ms_list

        to_replace_index = contents_structure.index('{{PREV_UG_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = prev_ug_list

        configurations['title'] = title
        configurations['style'] = style
        configurations['hasBody'] = True


if __name__=='__main__':
    dispatcher(True)
