import utils
import approx.Sources.update_funding, approx.Sources.update_people, approx.Sources.update_pubs, approx.Sources.update_index

def execute_all(specific_file=''):
    all_files = {
        'update_index': approx.Sources.update_index.dispatcher,
        'update_pubs': approx.Sources.update_pubs.dispatcher,
        'update_people': approx.Sources.update_people.dispatcher,
        'update_funding': approx.Sources.update_funding.dispatcher
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
            'update_pubs',
            'update_people',
            'update_funding'
        ],
        call_back=execute_all,
        called_as_main=isMain,
        specific_file=specific_file,
        project_name='approx'
    )

if __name__=='__main__':
    dispatcher(isMain=True)

