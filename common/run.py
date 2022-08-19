from datetime import datetime
import logging
import os
from pathlib import Path
from shutil import rmtree
from typing import Any

import cv2

from common import make_genetic_algorithm_generator_class


logger = logging.getLogger(__file__)


def run(
    output_directory_path       : Path,
    genetic_algorithm_strategy  : Any,
    n_iterations_patience       : int   = 100,
    is_debug_mode               : bool  = False,
):
    if output_directory_path.exists():
        rmtree( output_directory_path )
    os.mkdir( f'{output_directory_path}' )

    last_rounded_score = ( 0, 0 )
    n_iterations_with_same_score = 0
    last_update_time = datetime.now()

    genetic_generator = make_genetic_algorithm_generator_class( genetic_algorithm_strategy )

    logger.info('Now running visual genetic algorithm')
    for generation, best_image_rgb, best_score, debug_info in genetic_generator:
        current_update_time = datetime.now()
        update_time_microseconds = ( current_update_time - last_update_time ).microseconds
        last_update_time = current_update_time

        # we want to use the score (commonly an equality percentage) and 3 decimals
        rounded_score = round( best_score * 100000 )
        rounded_score_string = str(rounded_score)
        score_string = f'{rounded_score_string[:2]}_{rounded_score_string[2:]}'
        report_string = f'gen_{generation}__dt_{update_time_microseconds}_ms__score_{score_string}'

        logger.info( report_string )
        cv2.imwrite( f'{output_directory_path}/{report_string}.png', best_image_rgb )
        if is_debug_mode and debug_info:
            debug_info.write(f'{output_directory_path}/{report_string}_')

        # if score does not change, have patience. When patience is over, break
        n_iterations_with_same_score += 1 if rounded_score == last_rounded_score else 0
        if n_iterations_with_same_score == n_iterations_patience:
            break

        last_rounded_score = rounded_score

    logger.info( 'DONE' )
