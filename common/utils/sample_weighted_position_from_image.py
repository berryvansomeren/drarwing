import random

from common.primitives.point import Point


def sample_weighted_position_from_image( diff_image ):
    image_height, image_width = diff_image.shape[ :2 ]

    pixel_coords = [ ]
    pixel_weights = [ ]
    for y in range( image_height ) :
        for x in range( image_width ) :
            pixel_probability = diff_image[ y ][ x ]
            pixel_coords.append( Point( x, y ) )
            pixel_weights.append( pixel_probability )

    position = random.choices( pixel_coords, weights = pixel_weights )[ 0 ]
    return position
