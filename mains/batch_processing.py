import itertools
import logging
from pathlib import Path

import common


ROOT_DIR                        = Path( __file__ ).parent.parent
DEFAULT_INPUT_IMAGE_PATH        = ROOT_DIR / '_input_images'
DEFAULT_OUTPUT_DIRECTORY_PATH   = ROOT_DIR / 'results'
DEFAULT_BRUSH_DIRECTORY         = ROOT_DIR / '_input_images/brushes'


UNSPLASH_IMAGES = [
    "calvin-mano-CXS27RrJObQ-unsplash.jpg",
    "damian-patkowski-T-LfvX-7IVg-unsplash.jpg",
    "elisa-stone-ceKhGIXOGtA-unsplash.jpg",
    "faris-mohammed-jeRcm7wI-Hw-unsplash.jpg",
    "jaime-spaniol-RvV6qccrbkA-unsplash.jpg",
    "jeremy-bishop-rigCO5cf22I-unsplash.jpg",
    "pine-watt-2Hzmz15wGik-unsplash.jpg",
    "ricardo-frantz-D9lDqguxy4Y-unsplash.jpg",
    "sagar-kulkarni-8Td8zBzoAfM-unsplash.jpg",
    "tim-mossholder-cO5-QcKIR9o-unsplash.jpg",
    "bailey-zindel-NRQV-hBF10M-unsplash.jpg",
]


def painting():
    brush_names = [
        'sketch',
        'canvas',
        'watercolor',
        'oil',
    ]
    for image_name, brush_name in itertools.product( UNSPLASH_IMAGES, brush_names ):
        args = {
            'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / image_name,
            'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / f'{Path(image_name).stem}__{brush_name}',
            'algorithm_file_name' : 'painting',
            'is_pickling_desired' : False,
            'algorithm_arguments': {
                'brush_directory' : DEFAULT_BRUSH_DIRECTORY / brush_name,
            },
        }
        common.run_genetic_algorithm_by_name( **args )


def abstract():
    arg_pack = {
        'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'mario_yoshi.jpg',
        'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'mario_abstract',
        'algorithm_file_name' : 'abstract',
        'is_pickling_desired' : True,
    }
    common.run_genetic_algorithm_by_name(**arg_pack)


def pointillism():
    arg_packs = [
        {
            'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'mario_yoshi.jpg',
            'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'mario_pointillism',
            'algorithm_file_name' : 'pointillism',
            'is_pickling_desired' : True,
        },
        {
            'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'mario_yoshi.jpg',
            'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'mario_pointillism',
            'algorithm_file_name' : 'pointillism',
            'is_pickling_desired' : True,
        }
    ]
    for args in arg_packs:
        common.run_genetic_algorithm_by_name(**args)


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    painting()
    #pointillism()
    #abstract()