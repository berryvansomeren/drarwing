import argparse
import logging
import os
import shutil
from pathlib import Path
import itertools


logger = logging.getLogger(__name__)


def select_images_with_score_interval(
    input_image_path        : Path,
    output_directory_path   : Path,
    score_interval          : int,
) :
    """
    Filter your results to only include images
    that are at least a specific amount better than their predecessor.
    This is especially useful when selecting frames to use for creating Gifs.
    """

    os.makedirs( output_directory_path, exist_ok = True )

    def copy( source_file_path : Path, destination_directory_path : Path ) -> None:
        shutil.copy( source_file_path, destination_directory_path )

    def get_score_from_path( path : str ) -> float:
        # eat the string until we find the score number
        score_start_pointer = 0
        while path[score_start_pointer:score_start_pointer+len('score')] != 'score':
            score_start_pointer += 1
        score_start_pointer += len('score') + 1

        # now find the end of the score
        score_end_pointer = score_start_pointer
        while path[score_end_pointer] != '.':
            score_end_pointer += 1

        # convert pointers to actual int
        score_string = path[ score_start_pointer : score_end_pointer ]
        score = int(score_string)
        return score

    all_image_paths = sorted( input_image_path.glob('*.png') )
    copy( all_image_paths[0], output_directory_path )
    last_used_score = get_score_from_path(str(all_image_paths[0]))
    for previous_image_path, current_image_path in itertools.pairwise( all_image_paths ):
        current_score = get_score_from_path(str(current_image_path))
        if last_used_score - current_score >= score_interval:
            copy(current_image_path, output_directory_path)
            last_used_score = current_score


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument( '--input_directory_path',  type = str )
    parser.add_argument( '--output_directory_path', type = str )
    parser.add_argument( '--score_interval',        type = int, default = 100 )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.basicConfig( level = logging.INFO )
    logger.info( 'Parsing Args' )
    args = _get_args()
    logger.info( 'Selecting and Copying images' )
    select_images_with_score_interval(
        Path( args.input_directory_path ),
        Path( args.output_directory_path ),
        args.score_interval,
    )
    logger.info( 'Done' )
