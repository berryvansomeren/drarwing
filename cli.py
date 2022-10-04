import argparse
import json
import logging
from pathlib import Path

from common.run import run_genetic_algorithm_by_name


logger = logging.getLogger(__name__)


def _get_args():
    root_dir = Path(__file__).parent
    default_input_image_path        = root_dir / 'input_images/ship.jpg'
    default_output_directory_path   = root_dir / 'results'
    default_algorithm_file_name     = 'painting'
    default_brush_directory         = root_dir / 'input_images/brushes/oil'
    default_algorithm_arguments     = "{" + f'"brush_directory":"{default_brush_directory.as_posix()}"' + "}"

    logger.info( 'Parsing Args...' )
    parser = argparse.ArgumentParser()

    parser.add_argument( '--input_image_path',      type = str, default = default_input_image_path )
    parser.add_argument( '--output_directory_path', type = str, default = default_output_directory_path )
    parser.add_argument( '--algorithm_file_name',   type = str, default = default_algorithm_file_name )
    parser.add_argument( '--algorithm_arguments',   type = str, default = default_algorithm_arguments )

    parser.add_argument( '--n_iterations_patience', type = int, default = 100 )
    parser.add_argument( '--score_interval',        type = int, default = 500 )
    parser.add_argument( '--is_pickling_desired',   type = bool, default = True )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.basicConfig( level = logging.INFO )

    args = _get_args()
    run_genetic_algorithm_by_name(
        Path( args.input_image_path ),
        Path( args.output_directory_path ),
        args.algorithm_file_name,
        json.loads(args.algorithm_arguments),
        args.n_iterations_patience,
        args.score_interval,
        args.is_pickling_desired
    )
