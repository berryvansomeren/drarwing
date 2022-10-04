import logging
from pathlib import Path

from common.run import run_genetic_algorithm_by_name


def batch_processing_circle_evolution():

    """
    Just an ugly method to invoke drarwing multiple times through Python
    """

    root_dir = Path( __file__ ).parent.parent
    default_input_image_path = root_dir / 'input_images'
    default_output_directory_path = root_dir / 'results'

    def make_args(
            output_name: str,
            image_name : str,
    ):
        return {
            'input_image_path' : default_input_image_path / image_name,
            'output_directory_path' : default_output_directory_path / output_name,
            'algorithm_file_name' : 'abstract_art',
            'algorithm_arguments': {},
            'is_pickling_desired' : True,
        }

    # Just change this list to run the project multiple times in a loop
    args = [
        make_args( 'mario_yoshi_circle', 'mario_yoshi.jpg'),
    ]

    for arg_pack in args:
        run_genetic_algorithm_by_name(**arg_pack)


def batch_processing_painting():

    """
    Just an ugly method to invoke drarwing multiple times through Python
    """

    root_dir = Path( __file__ ).parent.parent
    default_input_image_path = root_dir / 'input_images'
    default_output_directory_path = root_dir / 'results'
    default_brush_directory = root_dir / 'input_images/brushes'

    def make_args_fixed_size(
            output_name: str,
            image_name : str,
            brushes_name : str,
    ):
        return {
            'input_image_path' : default_input_image_path / image_name,
            'output_directory_path' : default_output_directory_path / output_name,
            'algorithm_file_name' : 'painting',
            'is_pickling_desired' : True,
            'algorithm_arguments': {
                'brush_directory' : default_brush_directory / brushes_name,
                'autoscaling_brush_size' : False,
                'fixed_brush_size' : 35,
            },
        }

    def make_args_autoscaling(
            output_name: str,
            image_name : str,
            brushes_name : str,
    ):
        return {
            'input_image_path' : default_input_image_path / image_name,
            'output_directory_path' : default_output_directory_path / output_name,
            'algorithm_file_name' : 'painting',
            'is_pickling_desired' : True,
            'algorithm_arguments': {
                'brush_directory' : default_brush_directory / brushes_name,
                'autoscaling_brush_size' : True,
            },
        }

    # Just change this list to run the project multiple times in a loop
    args = [
        make_args_autoscaling( 'ship_oil_auto', 'ship.jpg', 'oil' ),
        make_args_autoscaling( 'ship_canvas_auto', 'ship.jpg', 'canvas' ),
        make_args_autoscaling( 'ship_sketches_auto', 'ship.jpg', 'sketch' ),
        make_args_autoscaling( 'ship_watercolor_auto', 'ship.jpg', 'watercolor' ),

        make_args_fixed_size( 'ship_oil_fixed', 'ship.jpg', 'oil' ),
        make_args_fixed_size( 'ship_canvas_fixed', 'ship.jpg', 'canvas' ),
        make_args_fixed_size( 'ship_sketches_fixed', 'ship.jpg', 'sketch' ),
        make_args_fixed_size( 'ship_watercolor_fixed', 'ship.jpg', 'watercolor' ),
    ]

    for arg_pack in args:
        run_genetic_algorithm_by_name(**arg_pack)


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    batch_processing_painting()