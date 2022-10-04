from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np

import common

"""
Note that this algorithm differs from painting in the sense that it can not really cache images 
because positions of circles can change through mutation. 
We then have to actually change the original image, instead of drawing on top of a cached image. 
"""

@dataclass
class Specimen:
    genes: List[ common.Circle ]
    diff_image : np.ndarray

Population = List[ Specimen ]


class AbstractArt( common.GeneticAlgorithm ):

    def __init__(
            self,
            target_image_rgb,
            n_population    = 10,
            n_genes         = 10,
            n_selection     = 3
    ):
        self.target_image   = cv2.cvtColor( target_image_rgb, cv2.COLOR_RGB2HSV )
        self._n_population  = n_population
        self._n_genes       = n_genes
        self._n_selection   = n_selection

        self.dx, self.dy = common.get_image_gradients_from_hsv(self.target_image)
        self._height, self._width, self._channels = self.target_image.shape
        self._min_radius = int( 0.05 * min(self._width, self._height) )
        self._max_radius = int( 0.15 * min(self._width, self._height) )

    def get_random_circle( self, diff_image ):
        circle_center = common.sample_weighted_position_from_image( diff_image )
        random_circle = common.random_circle(
            self._width,
            self._height,
            self._min_radius,
            self._max_radius
        )
        random_circle.position = circle_center
        random_circle.color = tuple(int(i) for i in self.target_image[circle_center.y][circle_center.x])

        return random_circle


    def get_initial_population( self ) -> Population:
        max_prob_image = np.ones(self.target_image.shape[ :2 ])
        initial_population = []
        for _i_specimen in range( self._n_population ):
            circles = [ ]
            for _i_gene in range( self._n_genes ) :
                circles.append( self.get_random_circle(max_prob_image) )
            initial_population.append( Specimen( circles, max_prob_image ) )
        return initial_population


    def apply_crossover( self, population : Population ) -> Population:
        return common.simple_copy_padding( population, self._n_population )


    def apply_mutation_inplace( self, population : Population ):

        # color
        def mutation__shift_color_hue( circle : common.Circle ) -> None:
            circle.color = common.random_shift_color_hue( color = circle.color, max_shift = 3 )

        def mutation__shift_color_saturation( circle : common.Circle ) -> None:
            circle.color = common.random_shift_color_saturation( color = circle.color, max_shift = 5 )

        def mutation__shift_color_value( circle : common.Circle ) -> None:
            circle.color = common.random_shift_color_value( color = circle.color, max_shift = 5 )

        def mutation__random_color( circle : common.Circle ) -> None:
            circle.color = common.random_hsv_color()

        # position
        def mutation__shift_position_x( circle : common.Circle ) -> None:
            circle.position.x = int( common.random_shift_within_range(
                value = circle.position.x,
                max_shift = 10,
                range_min = 0,
                range_max = self._width
            ) )

        def mutation__shift_position_y( circle : common.Circle ) -> None:
            circle.position.y = int( common.random_shift_within_range(
                value = circle.position.y,
                max_shift = 10,
                range_min = 0,
                range_max = self._height
            ) )

        def mutation__random_position( circle : common.Circle ) -> None:
            circle.position = common.random_point( self._width, self._height )

        # radius
        def mutation__shift_radius( circle : common.Circle ) -> None:
            circle.radius = int( common.random_shift_within_range(
                value = circle.radius,
                max_shift = 3,
                range_min = self._min_radius,
                range_max = self._max_radius
            ) )

        def mutation__random_radius( circle : common.Circle ) -> None:
            circle.radius = common.random_circle_radius( self._min_radius, self._max_radius )

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
            common.mutate_specimen_inplace(
                specimen,
                weighted_mutations,
                lambda : self.get_random_circle( specimen.diff_image ),
                p_add = 0,
                p_del = 0,
            )


    def get_fitness( self, population : Population ) -> common.FitnessScores:
        population_fitnesses = []
        for specimen in population:
            specimen_image = self.draw_specimen( specimen )
            absolute_difference_image = common.get_absolute_difference_image( specimen_image, self.target_image )
            specimen.diff_image = absolute_difference_image
            fitness = common.get_fitness_from_absolute_difference_image( absolute_difference_image )
            population_fitnesses.append(fitness)
        return population_fitnesses


    def apply_selection( self, population: Population, fitness_scores: common.FitnessScores ) -> Tuple[ Population, common.FitnessScores ] :
        return common.select_top_n( population, fitness_scores, self._n_selection )


    def draw_specimen( self, specimen: Specimen ) -> np.ndarray :
        # we redraw the entire image,
        # because any gene could have been mutated
        blank_image = np.zeros_like( self.target_image )
        blank_image.fill( 255 )
        hsv_image = cv2.cvtColor( blank_image, cv2.COLOR_RGB2HSV )
        for circle in specimen.genes:
            common.draw_circle_on_image( circle, hsv_image )
        return hsv_image


    def get_specimen_image_rgb( self, specimen: Specimen ) -> np.ndarray:
        hsv_image = self.draw_specimen(specimen)
        rgb_image = cv2.cvtColor( hsv_image, cv2.COLOR_HSV2RGB )
        return rgb_image


def get(target_image, **kwargs):
    return AbstractArt( target_image, **kwargs )