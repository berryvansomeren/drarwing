import argparse
import logging
import pickle
from pathlib import Path

import cv2
import numpy as np

import common
from genetic_algorithms.painting import Painting


logger = logging.getLogger(__name__)


def redraw_painting(
        specimen : Painting.Specimen,
        scale: float,
        result_image: np.ndarray
) -> np.ndarray:

    """
    Redraws a painting by using scaled versions of the original brushes.
    As long as the brush texture is available at larger resolutions,
    this allows you to make higher resolution versions of your images.
    Even if some of the brushes are drawn at scales larger than the original texture resolution,
    the image detail improve drastically as the larger brushes are painted over with smaller images.
    """

    def int_scale(v):
        return int( v * scale )

    n_oversized_brushes = 0
    for brush in specimen.brushes:

        # we will draw the brush at a new size
        brush_texture = common.get_global_brush_textures()[brush.texture_index]

        # note that brush width and height are expected to be equal
        original_brush_size = brush_texture.shape[0]
        brush.size = int_scale(brush.size)

        brush.position = common.Point(
            int_scale(brush.position.x),
            int_scale(brush.position.y),
        )

        if brush.size > original_brush_size:
            logger.warning(
                f'Brush with texture index {brush.texture_index} '
                f'is desired with size {brush.size}, '
                f'but has an original size of {original_brush_size}. '
                'Perhaps you need a lower target resolution, '
                'or higher resolution brush textures.'
            )
            n_oversized_brushes += 1

        common.draw_brush_on_image( brush, result_image )

    # As long as oversized brushes disappear in the background when they are painted over with smaller brushes,
    # having oversized brushes is not a problem.
    logger.info(f'Encountered {n_oversized_brushes}/{len(specimen.brushes)} oversized brushes')
    return result_image


def redraw_painting_with_new_width(
        input_result_pickle_path : Path,
        new_width: int,
        output_result_path : Path,
        brush_directory : Path,
) -> None:

    # We can only redraw the specimen if it was written as pickle file
    with open( input_result_pickle_path, 'rb' ) as pickle_file :
        specimen = Painting.Specimen(**pickle.load( pickle_file ))

    original_image_height, original_image_width = specimen.cached_image.shape[ :2 ]
    scale = new_width / original_image_width
    result_image_shape = (
        int(original_image_height * scale),
        int(original_image_width * scale ),
        3
    )
    result_image = np.zeros( result_image_shape, dtype = np.uint8 )
    result_image.fill(255)

    common.preload_brush_textures( brush_directory )

    result_image = redraw_painting(
        specimen,
        scale,
        result_image
    )

    cv2.imwrite( str(output_result_path), result_image )


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument( '--input_result_pickle_path', type = str )
    parser.add_argument( '--new_width', type = int )
    parser.add_argument( '--output_result_path', type = str )
    parser.add_argument( '--brush_directory', type = str )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.basicConfig( level = logging.INFO )
    logger.info( 'Parsing Args' )
    args = _get_args()
    logger.info( 'Selecting and Copying images' )
    redraw_painting_with_new_width(
        Path( args.input_result_pickle_path ),
        args.new_width,
        Path( args.output_result_path ),
        Path( args.brush_directory )
    )
    logger.info( 'Done' )