from datetime import datetime
import logging
import os
from pathlib import Path
import pickle
from runpy import run_path
from shutil import rmtree
from typing import Any, Dict, Optional

import cv2

from genetic_algorithms.common.genetic_algorithm_protocol import GeneticAlgorithm
from genetic_algorithms.common.genetic_algorithm_generator import make_genetic_algorithm_generator


logger = logging.getLogger(__name__)


DECIMALS = 3
SCORE_MULTIPLIER = 10 ** DECIMALS


def run_genetic_algorithm_strategy(
    output_directory_path       : Path,
    genetic_algorithm_strategy  : GeneticAlgorithm,
    n_iterations_patience       : int,
    score_interval              : int,
    is_pickling_desired         : bool,
    termination_score           : int,
) -> Any:
    last_rounded_score = 100 * SCORE_MULTIPLIER
    last_written_score = last_rounded_score
    n_iterations_with_same_score = 0
    last_update_time = datetime.now()

    genetic_generator = make_genetic_algorithm_generator( genetic_algorithm_strategy )

    def write_results(report_string, best_image_rgb, best_specimen_raw):
        cv2.imwrite( f'{output_directory_path}/{report_string}.png', best_image_rgb )
        # store pickled specimen if desired
        if is_pickling_desired :
            pickle_file_path = f'{output_directory_path}/{report_string}.pickle'
            with open( pickle_file_path, 'wb' ) as pickle_file :
                pickle.dump( best_specimen_raw.__dict__, pickle_file )

    logger.info('Running visual genetic algorithm')
    start_time = datetime.now()
    best_specimen_raw = None  # just to make sure that the variable exists in case the generator is empty
    for generation, best_image_rgb, best_score, best_specimen_raw in genetic_generator:
        current_update_time = datetime.now()
        update_time_microseconds = ( current_update_time - last_update_time ).microseconds
        last_update_time = current_update_time

        # we want to use the score (commonly an equality percentage) and 3 decimals
        rounded_score = round( best_score * 100 * SCORE_MULTIPLIER )
        report_string = f'gen_{generation:06d}__dt_{update_time_microseconds}_ms__score_{rounded_score}'

        logger.info( report_string )

        # if score does not change, have patience.
        if rounded_score == last_rounded_score:
            n_iterations_with_same_score += 1
        else:
            n_iterations_with_same_score = 0

            # We only write images if they show enough improvement compared to the last written one
            if last_written_score - rounded_score >= score_interval:
                write_results( report_string, best_image_rgb, best_specimen_raw)
                last_written_score = rounded_score

        # if ran out of patience, write the final result, and break
        if (
            n_iterations_with_same_score == n_iterations_patience
            or rounded_score <= termination_score
        ):
            write_results( report_string, best_image_rgb, best_specimen_raw)
            logger.info( 'Ran out of patience' )
            break

        last_rounded_score = rounded_score

    end_time = datetime.now()
    convergence_time = end_time - start_time
    logger.info( f'Converged in {convergence_time.seconds} seconds.' )
    logger.info( 'DONE' )
    return best_specimen_raw


def _load_get_function_from_python_file( path : Path ):
    module   = run_path( str( path ) )
    f_get    = module.get( 'get' )
    return f_get


def run_genetic_algorithm_by_name(
        input_image_path        : Path,
        output_directory_path   : Path,
        algorithm_file_name     : str,
        algorithm_arguments     : Optional[Dict] = None,
        n_iterations_patience   : int   = 100,
        score_interval          : int   = 500,
        is_pickling_desired     : bool  = True,
        termination_score       : int   = 3500
) -> Any:

    logger.info( f'Loading input image from {input_image_path}' )
    target_image = cv2.imread( str( input_image_path ) )
    assert target_image is not None, f"Could not read target_image: {input_image_path}"

    logger.info( f'Ensuring an empty output directory' )
    if output_directory_path.exists():
        rmtree( output_directory_path )
    os.mkdir( f'{output_directory_path}' )

    root_directory_path = Path(__file__).parent.parent.parent
    logger.info( f'Looking for algorithm with name "{algorithm_file_name}"' )
    algorithm_file_path = Path(f'{root_directory_path}/genetic_algorithms/impl/{algorithm_file_name}.py')
    logger.info( f'Loading algorithm from {algorithm_file_path}' )
    f_get = _load_get_function_from_python_file( algorithm_file_path )

    algorithm_arguments = algorithm_arguments or { }
    genetic_algorithm = f_get(target_image, **algorithm_arguments)

    result = run_genetic_algorithm_strategy(
        output_directory_path,
        genetic_algorithm,
        n_iterations_patience,
        score_interval,
        is_pickling_desired,
        termination_score
    )
    return result


def run_genetic_algorithm_pointillism(
        input_image_path        : Path,
        output_directory_path   : Path,
        algorithm_file_name     : str,
        algorithm_arguments     : Optional[Dict] = None,
        n_iterations_patience   : int   = 100,
        score_interval          : int   = 500,
        is_pickling_desired     : bool  = False,
        termination_score       : int   = 3500
) -> Any:
    logger.info( f'Loading input image from {input_image_path}' )
    target_image = cv2.imread( str( input_image_path ) )
    assert target_image is not None, f"Could not read target_image: {input_image_path}"

    logger.info( f'Ensuring an empty output directory' )
    if output_directory_path.exists():
        rmtree( output_directory_path )
    os.mkdir( f'{output_directory_path}' )

    from genetic_algorithms.impl.pointillism import get as f_get

    algorithm_arguments = algorithm_arguments or { }
    genetic_algorithm = f_get(target_image, **algorithm_arguments)

    result = run_genetic_algorithm_strategy(
        output_directory_path,
        genetic_algorithm,
        n_iterations_patience,
        score_interval,
        is_pickling_desired,
        termination_score
    )
    return result
