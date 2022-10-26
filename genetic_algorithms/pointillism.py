import copy
from dataclasses import dataclass
import math

import cv2
import numpy as np

import common


class Pointillism( common.SimpleGeneticAlgorithmBase ):

    """
    Pointillism

    We improve a painting iteratively by adding more points.
    Points are actually ellipses that roughly follow the gradient of the image.
    Colors are not directly copied form the target image,
    but retrieved from a palette that consists of a limited number
    of variations on colors from the target image
    """

    @dataclass
    class Specimen :
        cached_image: np.ndarray
        diff_image: np.ndarray


    def __init__(
            self,
            target_image,
            use_hsv = False,
            short_axis_size = None,
            long_axis_multiplier = 0.005,
            long_axis_exponent = 0.5
    ):
        self.use_hsv = use_hsv
        if self.use_hsv:
            target_image = cv2.cvtColor( target_image, cv2.COLOR_BGR2HSV )
        super().__init__(target_image)
        self._target_gradient = common.ImageGradient( self._target_image, is_hsv = self.use_hsv )
        self._color_palette = common.ColorPalette( self._target_image )

        if short_axis_size is None:
            # size of dots is based on shortest extend of width and height
            min_extend = min( self._target_image.shape[ :2 ] )
            self._short_axis_size = int( math.ceil( min_extend / 1000 ) )
        else:
            self._short_axis_size = short_axis_size

        self._long_axis_multiplier = long_axis_multiplier
        self._long_axis_exponent = long_axis_exponent

    def get_initial_population( self ) -> common.Population:
        blank_image = common.get_blank_image_like( self._target_image, use_hsv = self.use_hsv )
        abs_diff_image = common.get_absolute_difference_image( blank_image, self._target_image )

        initial_population = [
            self.Specimen( cached_image = copy.deepcopy( blank_image ), diff_image = abs_diff_image )
            for _ in range( self._n_population )
        ]
        return initial_population

    def _sample_new_ellipse( self, diff_image ):
        position = common.sample_weighted_position_from_image( diff_image )
        target_color = common.get_color_from_image( self._target_image, position )
        color = self._color_palette.get_matching_color_with_probabilities( target_color )
        angle = self._target_gradient.get_direction( position ) + 90

        gradient_magnitude = self._target_gradient.get_magnitude( position )
        long_axis_addition = self._long_axis_multiplier * ( gradient_magnitude ** self._long_axis_exponent )
        long_axis = int( math.ceil( self._short_axis_size + long_axis_addition ) )

        return common.Ellipse(
            color = color,
            position = position,
            axes = ( long_axis, self._short_axis_size ),
            angle = angle,
        )

    def apply_mutation_inplace( self, population : common.Population ):
        for specimen in population:
            new_ellipse = self._sample_new_ellipse( specimen.diff_image )
            common.draw_ellipse_on_image( new_ellipse, specimen.cached_image )

    def get_specimen_image_rgb( self, specimen: Specimen ) -> np.ndarray:
        # Since we work in HSV color space for this algorithm,
        # we have to convert to RGB before returning the image
        result_image = specimen.cached_image
        if self.use_hsv:
            result_image = cv2.cvtColor( result_image, cv2.COLOR_HSV2BGR )
        return result_image


def get(target_image, **kwargs):
    return Pointillism(target_image)