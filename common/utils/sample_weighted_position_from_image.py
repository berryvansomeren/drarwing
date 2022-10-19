from common.primitives.point import Point

import numpy as np


def sample_weighted_position_from_image( diff_image ) -> Point:
    flat_indices = np.arange( np.product( diff_image.shape ) )
    flat_weights = diff_image.ravel()
    sum_weights = np.sum( flat_weights )
    flat_probabilities = flat_weights / sum_weights
    random_flat_index = np.random.choice(flat_indices, p=flat_probabilities )
    # convert 1D index to 2D index
    position = np.unravel_index( random_flat_index, diff_image.shape )
    return Point( int( position[1]), int(position[0]) )
