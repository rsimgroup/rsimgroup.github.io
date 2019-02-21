import json
import codecs
import copy
import os
from .HTMLUtils import HTMLUtils as tags
from .BibtexUtils import BibtexUtils as bib_utils
from .TextGenerator import TextGenerator as text_gen


class JSONUtils:
    """
    Defines helper functions used by JSONInterface class
    """
    @staticmethod
    def sort_by_keys(list_of_dictionaries, key1='', key2='', reverse=True):
        if key1 == 'time':
            text_gen.time_does_not_exist()
            return bib_utils.sort_by_keys(list_of_dictionaries, 'year', key2, reverse)
        return bib_utils.sort_by_keys(list_of_dictionaries, key1, key2, reverse)

    @staticmethod
    def replace_with(list_of_dictionaries, key, original='', replace_with=''):
        for item in list_of_dictionaries:
            if item[key] == original:
                item[key] = replace_with




class JSONInterface:
    def __init__(self, file_path, target):
        """
        Target and file path must be specified
        :param target: a string
        :param file_path: string
        :return: None
        """
        if target == 'people' or target == 'news':
            with codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path), mode='r', encoding='utf-8') as file:
                temp_list = json.load(file)
        else:
            raise ValueError('target_file for load_file function must be specified!')
        self.json_object = temp_list
        self.target_file = target

    def extract_list(self, type='', project=''):
        """
        Extract the list from files based on the criteria supplied
        :param type: a string,
            this parameter is used for people.json only and must be supplied when used for people.json,
            as people is a dictionary of lists but news is a list of dictionaries
        :param project: a string, choose from '', 'approx' and 'specialization'
        :return: a list of dictionaries
        """

        if self.target_file == 'people':
            if type == '':
                raise ValueError('type parameter for extract_list function must be specified if the function is used to process people.json')
            if project != '':
                return [
                    item for item in self.json_object[type] if
                    'projects' in item and (  # this is to check if 'projects' is specified
                            project in item['projects'] or
                            project in item.get('_only_at_', [])
                    )
                ]
            else:
                return [item for item in self.json_object[type] if '_only_at_' not in item]

        elif self.target_file == 'news':
            if project != '':
                return [
                    item for item in self.json_object if
                    'projects' in item and (  # this is to check if 'projects' is specified
                            project in item['projects'] or
                            project in item.get('_only_at_', [])
                    )
                ]
            else:
                return [item for item in self.json_object if '_only_at_' not in item]
        else:
            return []


    def generate_faculty_html(self, faculty_list, sort_by=''):

        # SORTING DISABLED FOR FACULTY
        if sort_by != '':
            sorted_list = JSONUtils.sort_by_keys(faculty_list, sort_by, reverse=True)
        else:
            sorted_list = faculty_list
        temp_list = []
        flag = 0
        for item in sorted_list:
            faculty_name = item['name']
            faculty_link = item['url']
            image_link = item['image']['url']
            image_width = item['image']['width']
            image_height = item['image']['height']
            image_alt = faculty_name + '\'s Picture'

            temp = []
            if flag == 0:
                temp.append('<tr>')

            image = tags.img(alt=image_alt, height=image_height, width=image_width, src=image_link)
            link = tags.a(content=faculty_name, href=faculty_link)
            temp.append(
                tags.td(content=image, class_is='align_text_right entry_width')
            )
            temp.append(
                tags.td(content=link, class_is='style12 entry_width')
            )
            # this part is for horizontal alignment
            if flag == 1:
                temp.append('</tr>')
            flag = 0 if flag == 1 else 1
            temp_list.extend(temp)

        if flag == 0:
            temp_list.append('</tr>')


        return temp_list

    def generate_current_graduate_html(self, curr_grad_list, sort_by='year'):

        if sort_by == '':
            sorted_list = curr_grad_list
        else:
            sanitized_list = copy.deepcopy(curr_grad_list)
            # This sanitizing is needed since if there are illegal values the sorting will abort
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key=sort_by, original='', replace_with='0')
            sorted_list = JSONUtils.sort_by_keys(sanitized_list, sort_by, reverse=True)
        temp_list = []
        flag = 0
        for item in sorted_list:
            grad_name = item['name']
            grad_link = item['url']
            image_link = item['image']['url']
            image_width = item['image']['width']
            image_height = item['image']['height']
            image_alt = grad_name + '\'s Picture'

            temp = []
            if flag == 0:
                temp.append('<tr>')

            image = tags.img(alt=image_alt, height=image_height, width=image_width, src=image_link)
            link = tags.a(content=grad_name, href=grad_link)
            temp.append(
                tags.td(content=image, class_is='align_text_right entry_width')
            )
            temp.append(
                tags.td(content=link, class_is='style12 entry_width')
            )

            if flag == 1:
                temp.append('</tr>')
            flag = 0 if flag == 1 else 1
            temp_list.extend(temp)

        if flag == 0:
            temp_list.append('</tr>')
        return temp_list

    def generate_current_collaborator_html(self, curr_collab_list, sort_by='name'):
        if sort_by == '':
            sorted_list = curr_collab_list
        else:
            sanitized_list = copy.deepcopy(curr_collab_list)
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key=sort_by, original='', replace_with='a')

            sorted_list = JSONUtils.sort_by_keys(sanitized_list, sort_by, reverse=False)

        temp_list = []
        flag = 0
        for item in sorted_list:
            collab_name = item['name']
            collab_link = item['url']
            image_link = item['image']['url']
            image_width = item['image']['width']
            image_height = item['image']['height']
            image_alt = collab_name + '\'s Picture'

            temp = []
            if flag == 0:
                temp.append('<tr>')

            image = tags.img(alt=image_alt, height=image_height, width=image_width, src=image_link)
            link = tags.a(content=collab_name, href=collab_link)
            temp.append(
                tags.td(content=image, class_is='align_text_right entry_width')
            )
            temp.append(
                tags.td(content=link, class_is='style12 entry_width')
            )

            if flag == 1:
                temp.append('</tr>')
            flag = 0 if flag == 1 else 1
            temp_list.extend(temp)

        if flag == 0:
            temp_list.append('</tr>')
        return temp_list

    def generate_graduated_phd_html(self, grad_phd_list, sort_by='year'):
        if sort_by == '':
            sorted_list = grad_phd_list
        else:
            sanitized_list = copy.deepcopy(grad_phd_list)
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key=sort_by, original='', replace_with='0')
            sorted_list = JSONUtils.sort_by_keys(sanitized_list, sort_by, reverse=True)

        temp_list = []
        for item in sorted_list:
            phd_name = item['name']
            phd_link = item['url']
            phd_time = item['year']
            phd_employment = item['employment']
            thesis_title = item['thesis']['title']
            thesis_link = item['thesis']['url']
            image_link = item['image']['url']
            image_width = item['image']['width']
            image_height = item['image']['height']
            image_alt = phd_name + '\'s Picture'

            if phd_link != '':
                phd_link_entry = tags.a(content=phd_name, href=phd_link, class_is='approx_people_style')
            else:
                phd_link_entry = tags.span(content=phd_name)
            phd_link_entry += ', Ph.D. ' + phd_time + '&nbsp; <br />'

            if thesis_link != '':
                thesis_link_entry = tags.a(href=thesis_link, class_is='approx_people_style', content=tags.span(content=thesis_title)+'<br />')
            else:
                thesis_link_entry = tags.span(content=thesis_title) + '<br />'

            image = tags.img(alt=image_alt, height=image_height, width=image_width, src=image_link)
            image_td = tags.td(content=image)
            phd_td = tags.td(content=phd_link_entry+'Ph.D. thesis:&nbsp;'+thesis_link_entry+'First Employment: &nbsp;'+phd_employment, class_is='style12')
            temp_list.append(tags.tr(content=image_td+phd_td))

        return temp_list

    def generate_graduated_ms_html(self, grad_ms_list, sort_by='year'):
        if sort_by == '':
            sorted_list = grad_ms_list
        else:
            sanitized_list = copy.deepcopy(grad_ms_list)
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key=sort_by, original='', replace_with='0')
            sorted_list = JSONUtils.sort_by_keys(sanitized_list, sort_by, reverse=True)

        temp_list = []
        for item in sorted_list:
            grad_name = item['name']
            grad_time = item['year']

            temp_list.append(
                tags.p(content=grad_name+', M.S.'+grad_time+'&nbsp; <br />', class_is='style12 paragraph_margin')
            )
        return temp_list

    def generate_graduated_ug_html(self, grad_ug_list, sort_by='name'):
        if sort_by == '':
            sorted_list = grad_ug_list
        else:
            sanitized_list = copy.deepcopy(grad_ug_list)
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key=sort_by, original='', replace_with='a')
            sorted_list = JSONUtils.sort_by_keys(sanitized_list, sort_by, reverse=False)

        temp_list = []
        for item in sorted_list:
            ug_name = item['name']
            temp_list.append(tags.p(content=ug_name, class_is='style12 paragraph_margin'))
        return temp_list

    def generate_news_html(self, news_list, sort_by=''):

        # SORTING IS DISABLED FOR NEWS AS SOME TIME METADATA IS MISSING!

        if sort_by == '':
            sorted_list = news_list
        else:
            sanitized_list = copy.deepcopy(news_list)
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key='year', original='', replace_with='0')
            JSONUtils.replace_with(list_of_dictionaries=sanitized_list, key='month', original='', replace_with='0')
            sorted_list = JSONUtils.sort_by_keys(sanitized_list, key1='year', key2='month', reverse=True)

        temp_list = []
        for item in sorted_list:
            p_tag = tags.p(content=item['content']+'&nbsp;&nbsp;', class_is='style12')
            temp_list.append(tags.li(content=p_tag))
        return temp_list


