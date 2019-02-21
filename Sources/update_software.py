from . import utils
import os 


def dispatcher(isMain=False):
    utils.Managing.ManageWrapper(
        add_content_from_function=addContents,
        script_file_name_is=__file__,
        isMain=isMain
    )


def addContents(configurations, base_structure, contents_structure, sources_path):

        configurations['title'] = 'Sarita Adve&#39;s Group: Software'
        configurations['hasBody'] = True
        configurations['style'] = """
        <style type="text/css">
        .small_font_size {
            font-size: small;
        }
        </style>
        """


if __name__=='__main__':
    dispatcher(True)
