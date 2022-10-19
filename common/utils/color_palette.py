import itertools
import random
import numpy as np
from sklearn.cluster import KMeans

from common.primitives.color import HSVColor


DEFAULT_HSV_DELTAS = itertools.product(
    [ 0, 10, -10 ], # Hue deltas
    [ 0, 10, -10 ], # Saturation deltas
    [ 0, 10, -10 ], # Value deltas
)


class HSVColorPalette:

    def __init__( self, image : np.ndarray, n_colors : int = 11, hsv_deltas = DEFAULT_HSV_DELTAS ):

        # determine the main colors in the image
        clustering_obj = KMeans(n_clusters=n_colors)
        clustering_obj.fit(image.reshape(-1,3))
        main_colors = np.array( clustering_obj.cluster_centers_ )

        # create variations on the main colors, using specified deltas
        palette = []
        for hsv_delta in hsv_deltas:
            new_colors = np.add(main_colors, hsv_delta)
            # Compensate for hsv boundaries
            # Since Hue is cyclical we fix it using a modulus
            new_colors[:,0] %= 180
            new_colors = np.minimum( new_colors, np.array([179, 255, 255]))
            new_colors = np.maximum( new_colors, np.array([  0,   0,   0]))
            palette.extend(new_colors)

        self.colors = np.array( palette )


    def get_matching_color_with_probabilities( self, color: HSVColor ):
        # use inverse distance as weight
        # weights are expected to be non-negative numbers
        np_color = np.array( color)
        distances = [ np.linalg.norm( np_color - palette_color ) for palette_color in self.colors ]
        max_distance = max( distances )
        color_weights = [ max_distance - distance for distance in distances ]
        color = random.choices( self.colors, weights = color_weights )[ 0 ]
        return color
