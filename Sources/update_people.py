from . import utils
import os
import json

def dispatcher(isMain=False):
    page = utils.Managing.Managing(
        source_path_is=os.path.dirname(__file__),
        content_replace_keywords_with=mergeFile,
        dump_file_name_is='dump/dump_main_people.html',
        content_file_name_is='contents_people.html',
        script_file_name_is=__file__,
        base_file_name_is='base.html',
        data_file_is='people.json')
    if isMain:
        page.execute_as_main(parent_manage_script_is='manage_main.py')
    else:
        page.execute_as_module()


def calculateFaculty(faculty_list, people_dict):
    '''
    This function populates faculty_list with html elements
    :param faculty_list: list of strings
    :param people_dict: dictionary, originally from the json file
    :return: None
    '''
    flag = 0
    for item in people_dict['Faculty']:
        faculty_name = item['Name']
        faculty_link = item['Source']
        image_link = item['Image']['link']
        image_width = item['Image']['width']
        image_height = item['Image']['height']
        image_alt = faculty_name + '\'s Picture'

        temp = []
        if flag == 0:
            temp.append('<tr>')
        temp.extend(
            [
                '<td class="people_style13_variant" style="width: 50%">',
                '<img alt="' + image_alt + '" height=' + image_height + ' width=' + image_width + ' src="' + image_link + '">',
                '</td>',
                '<td class="style12" style="width: 50%">',
                '<a href="' + faculty_link + '" class="approx_people_style">' + faculty_name + '</a>',
                '</td>'
            ]
        )
        if flag == 1:
            temp.append('</tr>')
        flag = 0 if flag == 1 else 1
        faculty_list.extend(temp)

    if flag == 0:
        faculty_list.append('</tr>')

def calculateCurrGrad(curr_grad_list, people_dict):
    '''
    This function populates curr_grad_list with html elements
    :param curr_grad_list: list of strings
    :param people_dict: dictionary, originally from the json file
    :return: None
    '''
    flag = 0
    for item in people_dict['Current graduate students']:
        grad_name = item['Name']
        grad_link = item['Source']
        image_link = item['Image']['link']
        image_width = item['Image']['width']
        image_height = item['Image']['height']
        image_alt = grad_name + '\'s Picture'

        temp = []
        if flag == 0:
            temp.append('<tr>')
        temp.extend(
            [
                '<td class="people_style13_variant people_width">',
                '<img alt="' + image_alt + '" height=' + image_height + ' width=' + image_width + ' src="' + image_link + '">',
                '</td>',
                '<td class="style12 people_width">',
                '<a href="' + grad_link + '">' + grad_name + '</a>',
                '</td>'
            ]
        )
        if flag == 1:
            temp.append('</tr>')
        flag = 0 if flag == 1 else 1
        curr_grad_list.extend(temp)

    if flag == 0:
        curr_grad_list.append('</tr>')

def calculateCurrCollab(curr_collab_list, people_dict):
    '''
    This function populates curr_collab_list with html elements
    :param curr_collab_list: list of strings
    :param people_dict: dictionary, originally from the json file
    :return: None
    '''
    flag = 0
    for item in people_dict['Current collaborators']:
        collab_name = item['Name']
        collab_link = item['Source']
        image_link = item['Image']['link']
        image_width = item['Image']['width']
        image_height = item['Image']['height']
        image_alt = collab_name + '\'s Picture'

        temp = []
        if flag == 0:
            temp.append('<tr>')
        temp.extend(
            [
                '<td class="people_style13_variant people_width">',
                '<img alt="' + image_alt + '" height=' + image_height + ' width=' + image_width + ' src="' + image_link + '">',
                '</td>',
                '<td class="style12 people_width">',
                '<a href="' + collab_link + '">' + collab_name + '</a>',
                '</td>'
            ]
        )
        if flag == 1:
            temp.append('</tr>')
        flag = 0 if flag == 1 else 1
        curr_collab_list.extend(temp)

    if flag == 0:
        curr_collab_list.append('</tr>')


def calculatePrevPHD(prev_phd_list, people_dict):
    '''
    This function populates prev_phd_list with html elements
    :param prev_phd_list: list of strings
    :param people_dict: dictionary, originally from the json file
    :return: None
    '''
    for item in people_dict["Graduated Ph.D. students"]:
        phd_name = item['Name']
        phd_link = item['Source']
        phd_time = item['Time']
        phd_employment = item['Employment']
        thesis_title = item['Thesis']['name']
        thesis_link = item['Thesis']['link']
        image_link = item['Image']['link']
        image_width = item['Image']['width']
        image_height = item['Image']['height']
        image_alt = phd_name + '\'s Picture'

        if phd_link != '':
            phd_link_entry = '<a href="'+phd_link+'" class="approx_people_style">'+phd_name+'</a>, Ph.D. '+phd_time+'&nbsp; <br />'
        else:
            phd_link_entry = '<span>'+phd_name+'</span>, Ph.D. '+phd_time+'&nbsp; <br />'

        if thesis_link != '':
            thesis_link_entry = '<a href="'+thesis_link+'" class="approx_people_style">'+'<span>'+thesis_title+'</span><br /></a>'
        else:
            thesis_link_entry = '<span>'+thesis_title+'</span><br /></a>'

        prev_phd_list.extend(
            [
                '<tr>',
                '<td>',
                '<img alt="' + image_alt + '" height=' + image_height + ' width=' + image_width + ' src="' + image_link + '">',
                '</td>',
                '<td class="style12">',
                phd_link_entry,
                'Ph.D. thesis:&nbsp;',
                thesis_link_entry,
                'First Employment: &nbsp;'+phd_employment,
                '</td>'
                '</tr>'
            ]
        )

def calculatePrevMS(prev_ms_list, people_dict):
    for item in people_dict["Graduated M.S. students"]:
        grad_name = item['Name']
        grad_time = item['Time']

        prev_ms_list.extend(
            [
                '<p class="style12 people_paragraph">',
                grad_name+', M.S. '+grad_time+'&nbsp; <br />',
                '</p>'
            ]
        )

def calculatePrevUG(prev_ug_list, people_dict):
    for item in people_dict["Graduated M.S. students"]:
        ug_name = item['Name']

        prev_ug_list.extend(
            [
                '<p class="style12 people_paragraph">',
                ug_name,
                '</p>'
            ]
        )

def mergeFile(configurations, base_structure, contents_structure, sources_path):

        with open(os.path.join(sources_path, 'people.json'), 'r') as people_item:
            people_dict = json.load(people_item)

        style = '''
        <style>
            .people_style13_variant {
                text-align: right;
            }
            .people_paragraph {
              margin-left: 0.5in;
              margin-top: -17px;
            }
            .people_width {
              width: 25%;
            }
        </style>
        '''

        title = 'Sarita Adve\'s Group: People'

        faculty_list = []
        calculateFaculty(faculty_list, people_dict)
        curr_grad_list = []
        calculateCurrGrad(curr_grad_list, people_dict)
        curr_collab_list = []
        calculateCurrCollab(curr_collab_list, people_dict)
        prev_phd_list = []
        calculatePrevPHD(prev_phd_list, people_dict)
        prev_ms_list = []
        calculatePrevMS(prev_ms_list, people_dict)
        prev_ug_list = []
        calculatePrevUG(prev_ug_list, people_dict)

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
