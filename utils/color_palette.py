import itertools
import random
import numpy as np

import cv2
from sklearn.cluster import KMeans

from primitives.color import HSVColor


DEFAULT_COLOR_DELTAS = itertools.product(
    [ 0, 10, -10 ], # B or Hue deltas
    [ 0, 30 ], # G or Saturation deltas
    [ 0 ], # R or Value deltas
)


def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))


def write_palette_image( palette, n_main_colors : int, out_path : str, is_hsv : bool, section_size = 50 ) -> None:
    n_total_colors = len( palette )
    n_variations = int( n_total_colors / n_main_colors )

    palette_width = n_variations * section_size
    palette_height = n_main_colors * section_size

    palette_image = np.zeros( ( palette_height, palette_width, 3 ), dtype = np.uint8 )
    palette_image.fill( 255 )  # Fill with white

    for i, color in enumerate( palette ):
        x_min = ( i // n_main_colors ) * section_size
        y_min = ( i % n_main_colors ) * section_size
        x_max = x_min + section_size
        y_max = y_min + section_size
        cv2.rectangle( palette_image, ( x_min, y_min ), ( x_max, y_max ), color, -1 )

    if is_hsv:
        palette_image = cv2.cvtColor( palette_image, cv2.COLOR_HSV2BGR )

    cv2.imwrite( out_path, palette_image )
    print(f'Wrote color palette to "{out_path}"')


class ColorPalette:

    def __init__(
            self,
            image : np.ndarray,
            is_hsv : bool,
            n_colors : int = 17,
            color_deltas = DEFAULT_COLOR_DELTAS,
            out_path = None,
    ):

        # determine the main colors in the image
        clustering_obj = KMeans(n_clusters=n_colors)
        clustering_obj.fit(image.reshape(-1,3))
        main_colors = np.array( clustering_obj.cluster_centers_ )

        # Sort the colors based on their similarity (Euclidean distance)
        reference_color = np.array( [ 0, 0, 0 ], dtype = np.uint8 )  # Black color as a reference
        color_similarity = np.array( [ color_distance( color, reference_color ) for color in main_colors ] )
        sorted_indices = np.argsort( color_similarity )
        main_colors = main_colors[ sorted_indices ]

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

        if out_path:
            write_palette_image( palette, n_colors, out_path, is_hsv )


    def get_matching_color_with_probabilities( self, color: HSVColor ):
        # use inverse distance as weight
        # weights are expected to be non-negative numbers
        np_color = np.array( color)
        distances = [ np.linalg.norm( np_color - palette_color ) for palette_color in self.colors ]
        max_distance = max( distances )
        color_weights = [ max_distance - distance for distance in distances ]
        color = random.choices( self.colors, weights = color_weights )[ 0 ]
        return color
