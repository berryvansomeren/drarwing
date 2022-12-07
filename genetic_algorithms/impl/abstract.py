import copy
from dataclasses import dataclass
import random
from typing import List

import cv2
import numpy as np

import genetic_algorithms.common as GA_common


class Abstract( GA_common.SimpleGeneticAlgorithmBase ):

    """
    Abstract

    Starting with a number of genes we try to evolve an approximation of our target image.
    Genes can be mutated, added and deleted.
    This approach is a "proper" genetic algorithm and differs from Painting and Pointillism,
    in that it does not simply paint on top of results from previous generations.
    Any circle could be changed from the previous generation through mutation.
    We have to actually redraw and replace the previous image, instead of drawing on top.
    This results in more abstract approximations of the target image,
    relying more on randomness in the changes applied.
    """

    @dataclass
    class Specimen :
        genes: List[ GA_common.Circle ]
        diff_image: np.ndarray
        cached_image: np.ndarray

    def __init__(
            self,
            target_image,
            n_population    = 10,
            n_genes         = 10,
            n_selection     = 3
    ):
        # We will convert the target image to HSV,
        # so that it is easier to also compute fitness score in HSV
        target_image_hsv = cv2.cvtColor( target_image, cv2.COLOR_BGR2HSV )
        super().__init__(
            target_image_hsv,
            n_population = n_population,
            n_selection = n_selection
        )
        self._n_genes = n_genes
        self._min_radius = int( 0.05 * min(self._width, self._height) )
        self._max_radius = int( 0.15 * min(self._width, self._height) )

    def _get_random_circle_radius( self ) -> float:
        return random.randint( self._min_radius, self._max_radius )

    def _get_random_circle( self, diff_image ) -> GA_common.Circle:

        position = GA_common.sample_weighted_position_from_image( diff_image )
        color = GA_common.get_color_from_image( self._target_image, position )
        radius = self._get_random_circle_radius()

        circle = GA_common.Circle(
            color = color,
            position = position,
            radius = radius,
        )
        return circle

    def get_initial_population( self ) -> GA_common.Population:
        # we store the blank hsv image to make it easy to reuse later
        self._blank_hsv_image = GA_common.get_blank_image_like( self._target_image, use_hsv = True )
        absolute_difference_image = GA_common.get_absolute_difference_image( self._blank_hsv_image, self._target_image )

        initial_population = []
        for _i_specimen in range( self._n_population ):
            circles = [ ]
            for _i_gene in range( self._n_genes ) :
                circles.append( self._get_random_circle( absolute_difference_image ) )
            initial_population.append( self.Specimen( circles, absolute_difference_image, self._blank_hsv_image ) )
        return initial_population


    def apply_mutation_inplace( self, population : GA_common.Population ):

        # color
        def mutation__shift_color_hue( circle : GA_common.Circle ) -> None:
            circle.color = GA_common.random_shift_color_hue( color = circle.color, max_shift = 3 )

        def mutation__shift_color_saturation( circle : GA_common.Circle ) -> None:
            circle.color = GA_common.random_shift_color_saturation( color = circle.color, max_shift = 5 )

        def mutation__shift_color_value( circle : GA_common.Circle ) -> None:
            circle.color = GA_common.random_shift_color_value( color = circle.color, max_shift = 5 )

        def mutation__random_color( circle : GA_common.Circle ) -> None:
            circle.color = GA_common.random_hsv_color()

        # position
        def mutation__shift_position_x( circle : GA_common.Circle ) -> None:
            circle.position.x = int( GA_common.random_shift_within_range(
                value = circle.position.x,
                max_shift = 10,
                range_min = 0,
                range_max = self._width
            ) )

        def mutation__shift_position_y( circle : GA_common.Circle ) -> None:
            circle.position.y = int( GA_common.random_shift_within_range(
                value = circle.position.y,
                max_shift = 10,
                range_min = 0,
                range_max = self._height
            ) )

        def mutation__random_position( circle : GA_common.Circle ) -> None:
            circle.position = GA_common.random_point( self._width, self._height )

        # radius
        def mutation__shift_radius( circle : GA_common.Circle ) -> None:
            circle.radius = int( GA_common.random_shift_within_range(
                value = circle.radius,
                max_shift = 3,
                range_min = self._min_radius,
                range_max = self._max_radius
            ) )

        def mutation__random_radius( circle : GA_common.Circle ) -> None:
            circle.radius = self._get_random_circle_radius()

        weighted_mutations = (
            # color
            ( 3, mutation__shift_color_hue          ),
            ( 1, mutation__shift_color_saturation   ),
            ( 1, mutation__shift_color_value        ),
            ( 1, mutation__random_color             ),
            # position
            ( 3, mutation__shift_position_x ),
            ( 3, mutation__shift_position_y ),
            ( 1, mutation__random_position  ),
            # radius
            ( 3, mutation__shift_radius     ),
            ( 1, mutation__random_radius    ),
        )

        for specimen in population :
            GA_common.mutate_specimen_inplace(
                specimen,
                weighted_mutations,
                lambda : self._get_random_circle( specimen.diff_image ),
                p_add = 0,
                p_del = 0,
            )


    def get_fitness( self, population : GA_common.Population ) -> GA_common.FitnessScores:
        # super class expects a cached image per specimen,
        # we have to update that image here,
        # before using the super class method for getting fitness scores
        for specimen in population:
            # we redraw the entire image per specimen,
            # because any gene could have been mutated
            specimen.cached_image = copy.deepcopy( self._blank_hsv_image )
            for circle in specimen.genes:
                GA_common.draw_circle_on_image( circle, specimen.cached_image )

        return super().get_fitness( population )


    def get_specimen_image_rgb( self, specimen: Specimen ) -> np.ndarray:
        # Since we work in HSV color space for this algorithm,
        # we have to convert to RGB before returning the image
        hsv_image = specimen.cached_image
        rgb_image = cv2.cvtColor( hsv_image, cv2.COLOR_HSV2BGR )
        return rgb_image


def get(target_image, **kwargs):
    return Abstract( target_image, **kwargs )