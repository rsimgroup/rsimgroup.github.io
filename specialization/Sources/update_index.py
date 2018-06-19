from Sources import utils
import os


def dispatcher(isMain=False):
    utils.Managing.ManageWrapper(
        add_content_from_function=addContents,
        script_file_name_is=__file__,
        isMain=isMain
    )


def addContents(configurations, base_structure, contents_structure, sources_path):
    configurations['title'] = 'Scalable Specialization'
    configurations['hasLeft'] = False
    configurations['hasBody'] = True
    configurations['style'] = """
        <style type="text/css">
        .hetero_index_span{
			color: rgb(51, 51, 102);
			text-align: center;
		}
		</style>
		"""


if __name__ == '__main__':
    dispatcher(True)
