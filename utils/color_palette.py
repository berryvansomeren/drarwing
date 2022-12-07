import itertools
import random
import numpy as np
from sklearn.cluster import KMeans

from primitives.color import HSVColor


DEFAULT_COLOR_DELTAS = itertools.product(
    [ 0, 10, -10 ], # B or Hue deltas
    [ 0, 10, -10 ], # G or Saturation deltas
    [ 0, 10, -10 ], # R or Value deltas
)


class ColorPalette:

    def __init__( self, image : np.ndarray, is_hsv = False, n_colors : int = 11, color_deltas = DEFAULT_COLOR_DELTAS ):

        # determine the main colors in the image
        clustering_obj = KMeans(n_clusters=n_colors)
        clustering_obj.fit(image.reshape(-1,3))
        main_colors = np.array( clustering_obj.cluster_centers_ )

        # create variations on the main colors, using specified deltas
        palette = []
        for current_delta in color_deltas:
            new_colors = np.add(main_colors, current_delta)

            # Compensate for hsv boundaries
            # Since Hue is cyclical we fix it using a modulus
            if is_hsv:
                new_colors[:,0] %= 180

            new_colors = np.minimum( new_colors, np.array([255, 255, 255]))
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
