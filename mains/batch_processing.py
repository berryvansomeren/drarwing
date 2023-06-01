import itertools
import logging
import pickle
from pathlib import Path

from genetic_algorithms.common.run import run_genetic_algorithm_by_name, run_genetic_algorithm_pointillism
from redraw import redraw_painting_at_4k, redraw_pointillism_at_4k
from genetic_algorithms.impl.pointillism import Pointillism

import cv2


logger = logging.getLogger(__name__)


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
        image_directory_name = f'{Path(image_name).stem}__{brush_name}'
        output_directory_path = DEFAULT_OUTPUT_DIRECTORY_PATH / image_directory_name
        brush_directory = DEFAULT_BRUSH_DIRECTORY / brush_name
        args = {
            'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / image_name,
            'output_directory_path' : output_directory_path,
            'algorithm_file_name' : 'painting',
            'is_pickling_desired' : False,
            'algorithm_arguments': {
                'brush_directory' : brush_directory,
            },
        }
        result = run_genetic_algorithm_by_name( **args )

        result_4k = redraw_painting_at_4k(
            specimen = result,
            brush_directory = args['algorithm_arguments']['brush_directory']
        )

        output_path_4k = f'{output_directory_path}/_{image_directory_name}__final_result_4k.png'
        cv2.imwrite( output_path_4k, result_4k )
        logger.info( f'Wrote 4k result to {output_path_4k}' )



def abstract():
    arg_pack = {
        'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'mario_yoshi.jpg',
        'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'mario_abstract',
        'algorithm_file_name' : 'abstract',
        'is_pickling_desired' : True,
    }
    run_genetic_algorithm_by_name( **arg_pack )


CITIES_IMAGES = [
    'denys-nevozhai-2vmT5_FeMck-unsplash.jpg'
]


def pointillism():
    arg_packs = [
        {
            'input_image_path' : DEFAULT_INPUT_IMAGE_PATH / 'cities/pawel-nolbert-4u2U8EO9OzY-unsplash.jpg',
            'output_directory_path' : DEFAULT_OUTPUT_DIRECTORY_PATH / 'city_1_pointillism',
            'algorithm_file_name' : 'pointillism',
            'is_pickling_desired' : True,
        },
    ]
    for args in arg_packs:
        result = run_genetic_algorithm_by_name( **args )
        result_4k = redraw_pointillism_at_4k(result)

        output_path_4k = f'{arg_packs[0]["output_directory_path"]}/final_result_4k.png'
        cv2.imwrite( output_path_4k, result_4k )
        logger.info( f'Wrote 4k result to {output_path_4k}' )


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    painting()
    pointillism()
    abstract()