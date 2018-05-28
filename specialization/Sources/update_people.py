import utils
import os

def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=addContents,
        dump_file_name_is='../people.html',
        content_file_name_is='contents_people.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
    )
    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()



def addContents(configurations, base_structure, contents_structure, sources_path):

        application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        interface = utils.JSONUtils.JSONInterface(people_json_path=os.path.join(application_path, 'Sources/people.json'))
        interface.load_file(target_file='people')

        style = '''
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
        '''

        title = 'Specialization: People'

        faculty_list = interface.generate_faculty_html(interface.extract_list(type='Faculty', project='specialization'))

        curr_grad_list = interface.generate_current_graduate_html(interface.extract_list(type='Current graduate students', project='specialization'))

        curr_collab_list = interface.generate_current_collaborator_html(interface.extract_list(type='Current collaborators', project='specialization'))

        prev_ug_list = interface.generate_graduated_ug_html(interface.extract_list(type='Past visiting students and undergraduate students', project='specialization'))


        to_replace_index = contents_structure.index('{{FACULTY_ITEM}}')
        contents_structure[to_replace_index:to_replace_index+1] = faculty_list

        to_replace_index = contents_structure.index('{{CURR_GRAD_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = curr_grad_list

        to_replace_index = contents_structure.index('{{CURR_COLLAB_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = curr_collab_list

        to_replace_index = contents_structure.index('{{PREV_UG_ITEM}}')
        contents_structure[to_replace_index:to_replace_index + 1] = prev_ug_list


        configurations['title'] = title
        configurations['style'] = style
        configurations['hasBody'] = True




if __name__=='__main__':
    dispatcher(True)