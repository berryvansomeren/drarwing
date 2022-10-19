import logging
from pathlib import Path

import common

ROOT_DIR                        = Path( __file__ ).parent.parent
DEFAULT_INPUT_IMAGE_PATH        = ROOT_DIR / '_input_images'
DEFAULT_OUTPUT_DIRECTORY_PATH   = ROOT_DIR / 'results'
DEFAULT_BRUSH_DIRECTORY         = ROOT_DIR / '_input_images/brushes'


def painting():
    # We invoke the same algorithm multiple times
    # with slightly different arguments.
    # This helper function removes some repetition for us
    def make_args(
            output_name: str,
            image_name : str,
            brushes_name : str,
    ):
        return {
            'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / image_name,
            'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / output_name,
            'algorithm_file_name' : 'painting',
            'is_pickling_desired' : True,
            'algorithm_arguments': {
                'brush_directory' : DEFAULT_BRUSH_DIRECTORY / brushes_name,
            },
        }

    args = [
        make_args( 'ship_sketch',       'ship.jpg', 'sketch' ),
        make_args( 'ship_canvas',       'ship.jpg', 'canvas' ),
        make_args( 'ship_watercolor',   'ship.jpg', 'watercolor' ),
        make_args( 'ship_oil',          'ship.jpg', 'oil' ),
    ]
    for arg_pack in args:
        common.run_genetic_algorithm_by_name(**arg_pack)


def abstract():
    arg_pack = {
        'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'mario_yoshi.jpg',
        'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'mario_abstract',
        'algorithm_file_name' : 'abstract',
        'is_pickling_desired' : True,
    }
    common.run_genetic_algorithm_by_name(**arg_pack)


def pointillism():
    arg_pack = {
        'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'mario_yoshi.jpg',
        'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'mario_pointillism',
        'algorithm_file_name' : 'pointillism',
        'is_pickling_desired' : True,
    }
    common.run_genetic_algorithm_by_name(**arg_pack)


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    #painting()
    #pointillism()
    abstract()