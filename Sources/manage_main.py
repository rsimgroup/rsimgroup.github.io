from . import utils
from . import update_software, update_funding, update_projects, update_people, update_pubs, update_news, update_index

def execute_all(specific_file=''):
    all_files = {
        'update_index': update_index.dispatcher,
        'update_news': update_news.dispatcher,
        'update_pubs': update_pubs.dispatcher,
        'update_people': update_people.dispatcher,
        'update_projects': update_projects.dispatcher,
        'update_software': update_software.dispatcher,
        'update_funding': update_funding.dispatcher
    }
    specific_function = all_files.get(specific_file, None)

    if specific_function != None:
        specific_function()
    else:
        for every_function in list(all_files.values()):
            every_function()


def dispatcher(isMain=False, specific_file=''):
    utils.FileDispatcher.FileDispatcher(
        file_array=[
            'update_index',
            'update_news',
            'update_pubs',
            'update_people',
            'update_projects',
            'update_software',
            'update_funding'
        ],
        call_back=execute_all,
        called_as_main=isMain,
        specific_file=specific_file
    )

if __name__=='__main__':
    dispatcher(isMain=True)

