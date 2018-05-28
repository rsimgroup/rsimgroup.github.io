import bibtexparser
from .HTMLUtils import HTMLUtils as tags
from .TextGenerator import TextGenerator as text_gen


class BibtexUtils:
    '''
    This class consists of static method only
    '''
    @staticmethod
    def convert_month_to_number(string):
        if string == '':
            return 0
        elif len(string) == 3:
            return {
                'Jan': 1,
                'Feb': 2,
                'Mar': 3,
                'Apr': 4,
                'May': 5,
                'Jun': 6,
                'Jul': 7,
                'Aug': 8,
                'Sep': 9,
                'Oct': 10,
                'Nov': 11,
                'Dec': 12
            }.get(string, 0)
        else:
            return {
                'January': 1,
                'February': 2,
                'March': 3,
                'April': 4,
                'May': 5,
                'June': 6,
                'July': 7,
                'August': 8,
                'September': 9,
                'October': 10,
                'November': 11,
                'December': 12
            }.get(string, 0)

    @staticmethod
    def convert_number_to_month(number, abbreviation='False'):
        string = str(number)
        if abbreviation:
            return {
                '1': 'Jan',
                '2': 'Feb',
                '3': 'Mar',
                '4': 'Apr',
                '5': 'May',
                '6': 'Jun',
                '7': 'Jul',
                '8': 'Aug',
                '9': 'Sep',
                '10': 'Oct',
                '11': 'Nov',
                '12': 'Dec'
            }.get(string, '')
        else:
            return {
                '1': 'January',
                '2': 'February',
                '3': 'March',
                '4': 'April',
                '5': 'May',
                '6': 'June',
                '7': 'July',
                '8': 'August',
                '9': 'September',
                '10': 'October',
                '11': 'November',
                '12': 'December'
            }.get(string, '')

    @staticmethod
    def surround_title_with_braces(string):
        return '{' + string + '}'

    @staticmethod
    def generate_string_author(author):
        '''
        Generates BibTex-format author string
        :param author: a list of strings -> each entry must be in the form of 'First_Name Middle_name Last_name'; or a string -> must also follow the same pattern
        :return: a string
        '''
        if isinstance(author, (list,)):
            formatted_author = []
            for author_item in author:
                temp_array = author_item.split()
                temp_array.insert(0, temp_array.pop())
                formatted_author.append((', '.join(temp_array[:2])+' '+' '.join(temp_array[2:])).rstrip())
            return ' and '.join(formatted_author)
        else:
            temp_array = author.split()
            temp_array.insert(0, temp_array.pop())
            formatted_author = (', '.join(temp_array[:2])+' '+' '.join(temp_array[2:])).rstrip()
            return formatted_author

    @staticmethod
    def get_bibtex_parser():
        '''
        Generates customized parser
        :return: customized BibTex parser
        '''
        parser = bibtexparser.bparser.BibTexParser()
        parser.ignore_nonstandard_types = False
        return parser

    @staticmethod
    def extract_list_author(author):
        '''
        Generates a list of authors.
        :param author: a string, must be separated by 'and'
        :return: a list of strings, each in the format of 'First_name Middle_name Last_name'
        '''
        if author == '':
            return ''
        temp_author = [' '.join(author_item.split(',')[::-1]) for author_item in author.split(' and ')]
        return [author_item.strip() for author_item in temp_author]

    @staticmethod
    def sort_by_keys(object, key1='year', key2='month', reverse=True):
        '''
        Sort the object and return the sorted result
        :param object: a list of dictionary
        :param key1: a string
        :param key2: a string
        :param reverse: bool
        :return: a list of dictionary
        '''
        if key1 == 'year' and key2 == 'month':
            sorted_object = sorted(
                object,
                key=lambda dictionary: (int(dictionary['year'].strip()), int(dictionary['month'].strip())),
                reverse=reverse
            )
            return sorted_object
        if key1 != '' and key2 != '':
            try:
                sorted_object = sorted(object, key=lambda dictionary: (dictionary[key1], dictionary[key2]), reverse=reverse)
                return sorted_object
            except KeyError:
                text_gen.at_least_one_sorted_error(key1, key2)
        if key1 != '':
            try:
                sorted_object = sorted(object, key=lambda dictionary: dictionary[key1], reverse=reverse)
                return sorted_object
            except KeyError:
                text_gen.sort_key_does_not_exist(key1)

        if key2 != '':
            try:
                sorted_object = sorted(object, key=lambda dictionary: dictionary[key2], reverse=reverse)
                return sorted_object
            except KeyError:
                text_gen.sort_key_does_not_exist(key2)
        else:
            sorted_object = object
            text_gen.sort_failed()
            return sorted_object

    @staticmethod
    def write_to_bibtex_file(file_path, object):
        '''
        Create a bibtex file and write to it
        :param file_path: a string
        :param object: an object -> should be a list of dictionary
        :return: None
        '''
        with open(file_path, 'w') as file:
            writer = bibtexparser.bwriter.BibTexWriter()
            database = bibtexparser.bibdatabase.BibDatabase()
            database.entries = object
            file.write(writer.write(database))

    @staticmethod
    def remove_braces(string):
        return string.strip('{').strip('}')



class BibtexInterface:
    def __init__(self,
                 msthesis_path='publication_bibtex/msthesis.bib',
                 paper_path='publication_bibtex/paper.bib',
                 phdthesis_path='publication_bibtex/msthesis.bib',
                 talk_path='publication_bibtex/talk.bib'
                 ):
        # Default must be overridden when used for project-level files. Examples see update_people and update_news in approx or specialization project
        self.msthesis_path = msthesis_path
        self.paper_path = paper_path
        self.phdthesis_path = phdthesis_path
        self.talk_path = talk_path

    def extract_msthesis_list(self, project=''):
        '''
        Generates a list of dictionaries based on the filtering criteria project
        :param project: a string of project
        :return: a list of dictionaries
        '''
        # must use customzied parser here
        parser = BibtexUtils.get_bibtex_parser()
        with open(self.msthesis_path, 'r') as file:
            msthesis = bibtexparser.load(file, parser).entries
        if project == '':
            return msthesis
        else:
            return [item for item in msthesis if project in item['projects']]

    def extract_paper_list(self, project=''):
        parser = BibtexUtils.get_bibtex_parser()
        with open(self.paper_path, 'r') as file:
            paper = bibtexparser.load(file, parser).entries
        if project == '':
            return paper
        else:
            return [item for item in paper if project in item['_projects']]

    def extract_phdthesis_list(self, project=''):
        parser = BibtexUtils.get_bibtex_parser()
        with open(self.phdthesis_path, 'r') as file:
            phdthesis = bibtexparser.load(file, parser).entries
        if project == '':
            return phdthesis
        else:
            return [item for item in phdthesis if project in item['projects']]

    def extract_talk_list(self, project=''):
        parser = BibtexUtils.get_bibtex_parser()
        with open(self.talk_path, 'r') as file:
            talk = bibtexparser.load(file, parser).entries
        if project == '':
            return talk
        else:
            return [item for item in talk if project in item['projects']]


    @staticmethod
    def get_all_paper_entries():

        # ID collision is handled by adding two arbitrary CAPITAL letters immediately after the original ID

        # precedence:
        #   entries preceded by _ has higher precedence than Google Scholar generated entries when displayed on webpage, as they are manually added rather than Google Scholar generated
        #   but when using bibtex directly for citation purposes, all _ entries should be removed
        #       _author > author
        #       _booktitle > booktitle
        #       _conference > journal + booktitle + organization + pages + publisher + volume + number -> respect the original content and structure when displaying instead of automatically generated ones
        #       _year > year; check if _year and _month is already in _conference, if true then do not display
        #       _month is in string form; normally do not display; for indexing and sorting purpose
        #       _publisher > publisher
        #       _statusnote should be placed immediately before _conference as supplementary information about the paper itself
        #       _italicsnote should be placed at the end
        #       _boldnote should be placed at the front of _italicsnote, if possible
        #       _volume > volume

        return [
            'ENTRYTYPE', 'ID',
            '_author', '_boldnote', '_booktitle', '_conference', '_italicsnote', '_month', '_projects', '_publisher', '_statusnote', '_title', '_url', '_volume', '_year',
            'author', 'booktitle', 'institution', 'journal', 'number', 'organization', 'pages', 'publisher', 'title', 'volume', 'year'
        ]

    @staticmethod
    def get_all_talk_entries():
        return ['ENTRYTYPE', 'ID', 'author', 'content', 'month', 'projects', 'title', 'year']

    @staticmethod
    def get_all_msthesis_entries():
        return ['ENTRYTYPE', 'ID', 'author', 'projects', 'title', 'url', 'year']

    @staticmethod
    def get_all_phdthesis_entries():
        return ['ENTRYTYPE', 'ID', 'author', 'italicsnote', 'month', 'projects', 'title', 'url', 'year']

    def generate_paper_html(self, paper_list):
        '''
        Generate HTML from a list of dictionaries whose attributes should be specified in respective functions get_all_*_entries above
        :param paper_list: a list of dictionaries
        :return: a list of strings
        '''

        # ALL ENTRIES CAN BE EMPTY

        # structure: title, author, statusnote, (conference)/(journal/booktitle + volume + number + pages + year). boldnote. statusnote

        paper_html = []
        for item in paper_list:

            # process title
            title = item['_title'] if '_title' in item else item['title']
            if title != '':
                title = tags.a(content=title, href=item['_url'])

            # process author
            author = ''
            if '_author' in item:
                author = item['_author']
            elif 'author' in item:
                author = item['author']
            author = ', '.join(BibtexUtils.extract_list_author(author))

            # process conference
            conference = item['_conference'] if '_conference' in item else ''

            if conference == '':
                if 'journal' in item:
                    conference = item['journal']
                elif '_booktitle' in item:
                    conference = item['_booktitle']
                elif 'booktitle' in item:
                    conference = item['booktitle']

                if '_volume' in item:
                    volume = 'vol. ' + item['_volume']
                elif 'volume' in item:
                    volume = 'vol. ' + item['volume']
                else:
                    volume = ''


                number = 'no. ' + item['number'] if 'number' in item else ''
                pages = item['pages'] if 'pages' in item else ''

                conference = tags.connect_elements(conference, volume, number, pages)

            # process year
            try:
                year = item['_year'] if '_year' in item else item['year']
            except KeyError:
                year = ''

            # process month
            month = str(item['_month']) if '_month' in item else ''

            if year not in conference:
                tags.connect_elements(conference, year)

            # process auxiliary notes
            status = item['_statusnote'] if '_statusnote' in item else ''
            bold = item['_boldnote'] if '_boldnote' in item else ''
            if bold != '':
                bold = tags.strong(content=bold)
            italics = item['_italicsnote'] if '_italicsnote' in item else ''
            if italics != '':
                italics = tags.em(content=italics)

            if year == '':
                year = '0'
            if month == '':
                month = '0'

            # this dictionary is used in sorting, since it is cleaned
            paper_html.append(
                {
                    'year': year,
                    'month': month,
                    'content': tags.li(content=tags.connect_elements(title, author, status+conference, bold, italics)+'<br/>&nbsp;<br/>', class_is='style12 pubs_margin')
                }
            )

        # sort the list after processing all items -> by default by time (year and month)
        return [item['content'] for item in BibtexUtils.sort_by_keys(paper_html, reverse=True)]

    def generate_phdthesis_html(self, phd_list):

        # structure: title, author, date, italicsnote
        phd_html = []
        for item in phd_list:
            title = BibtexUtils.remove_braces(item['title'])

            if 'url' in item:
                title = tags.a(content=title, href=item['url'])
            author = ', '.join(BibtexUtils.extract_list_author(item['author']))

            year = item['year'] if 'year' in item else ''
            month = item['month'] if 'month' in item else ''
            time = ''
            if year != '':
                if month != '':
                    time = BibtexUtils.convert_number_to_month(month) + ' ' + year
                else:
                    time = year

            italics = item['italicsnote'] if 'italicsnote' in item else ''
            html = tags.li(content=tags.connect_elements(title, author, time, italics)+'<br/>&nbsp;<br/>', class_is='style12 pubs_margin')

            if year == '':
                year = '0'
            if month == '':
                month = '0'

            phd_html.append({
                'year': year,
                'month': month,
                'content': html
            })

        return [item['content'] for item in BibtexUtils.sort_by_keys(phd_html, reverse=True)]

    def generate_msthesis_html(self, msthesis_list):

        # structure: title, author, year

        ms_html = []
        for item in msthesis_list:
            title = BibtexUtils.remove_braces(item['title'])
            if 'url' in item:
                title = tags.a(content=title, href=item['url'])

            author = item['author'] if 'author' in item else ''
            year = item['year'] if 'year' in item else ''

            html = tags.li(content=tags.connect_elements(title, author, year)+'<br/>&nbsp;<br/>', class_is='style12 pubs_margin')

            ms_html.append({
                'year': year,
                'content': html
            })
        return [item['content'] for item in BibtexUtils.sort_by_keys(ms_html, key1='year', key2='', reverse=True)]

    def generate_talk_html(self, talk_list):

        # structure: content
        talk_html = []
        for item in talk_list:
            month = item['month'] if 'month' in item else '0'
            year = item['year'] if 'year' in item else '0'
            talk_html.append({
                'month': month,
                'year': year,
                'content': tags.li(content=item['content']+'<br/>&nbsp;<br/>', class_is='style12 pubs_margin')
            })
        return [item['content'] for item in BibtexUtils.sort_by_keys(talk_html, reverse=True)]