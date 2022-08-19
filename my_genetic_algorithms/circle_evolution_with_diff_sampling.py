from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np

import common

@dataclass
class Specimen:
    genes: List[ common.Circle ]
    diff_image : np.ndarray

Population = List[ Specimen ]


class CircleEvolutionWithDiffSampling:

    target_image : np.ndarray

    _n_population   = 10
    _n_genes        = 1
    _n_selection    = 3

    _width : int
    _height : int
    _channels : int

    _min_radius : float
    _max_radius : float

    def __init__( self, target_image_rgb ):
        self.target_image = cv2.cvtColor( target_image_rgb, cv2.COLOR_RGB2HSV )
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
        random_circle.color = common.HSVColor(*(int(i) for i in self.target_image[circle_center.y][circle_center.x]))

        return random_circle


    def get_initial_population( self ) -> Population:
        max_prob_image = np.ones(self.target_image.shape[ :2 ])
        initial_population = []
        for _ in range( self._n_population ):
            circles = [ ]
            for _ in range( self._n_genes ) :
                circles.append( self.get_random_circle(max_prob_image) )
            initial_population.append( Specimen( circles, max_prob_image ) )
        return initial_population


    def apply_crossover( self, population : Population ) -> Population:
        return gal.simple_copy_padding( population, self._n_population )


    def apply_mutation_inplace( self, population : Population ):

        # color
        def mutation__shift_color_hue( circle : gal.Circle ) -> None:
            circle.color = gal.random_shift_color_hue( color = circle.color, max_shift = 3 )

        def mutation__shift_color_saturation( circle : gal.Circle ) -> None:
            circle.color = gal.random_shift_color_saturation( color = circle.color, max_shift = 5 )

        def mutation__shift_color_value( circle : gal.Circle ) -> None:
            circle.color = gal.random_shift_color_value( color = circle.color, max_shift = 5 )

        def mutation__random_color( circle : gal.Circle ) -> None:
            circle.color = gal.random_color()

        # position
        def mutation__shift_position_x( circle : gal.Circle ) -> None:
            circle.position.x = int( gal.random_shift_within_range(
                value = circle.position.x,
                max_shift = 10,
                range_min = 0,
                range_max = self._width
            ) )

        def mutation__shift_position_y( circle : gal.Circle ) -> None:
            circle.position.y = int( gal.random_shift_within_range(
                value = circle.position.y,
                max_shift = 10,
                range_min = 0,
                range_max = self._height
            ) )

        def mutation__random_position( circle : gal.Circle ) -> None:
            circle.position = gal.random_point( self._width, self._height )

        # radius
        def mutation__shift_radius( circle : gal.Circle ) -> None:
            circle.radius = int( gal.random_shift_within_range(
                value = circle.radius,
                max_shift = 3,
                range_min = self._min_radius,
                range_max = self._max_radius
            ) )

        def mutation__random_radius( circle : gal.Circle ) -> None:
            circle.radius = gal.random_circle_radius( self._min_radius, self._max_radius )

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
            gal.mutate_specimen_inplace(
                specimen,
                weighted_mutations,
                lambda : self.get_random_circle( specimen.diff_image ),
                p_add = 0.2,
                p_del = 0.1,
            )


    def get_fitness( self, population : Population ) -> common.FitnessScores:
        population_fitnesses = []
        for specimen in population:
            specimen_image = self.draw_specimen( specimen )
            absolute_difference_image = gal.get_absolute_difference_image( specimen_image, self.target_image )
            specimen.diff_image = absolute_difference_image
            fitness = gal.get_fitness_from_absolute_difference_image( absolute_difference_image )
            population_fitnesses.append(fitness)
        return population_fitnesses


    def apply_selection( self, population: Population, fitness_scores: gal.FitnessScores ) -> Tuple[ Population, gal.FitnessScores ] :
        return gal.select_top_n( population, fitness_scores, self._n_selection )


    def draw_specimen( self, specimen: Specimen ) -> np.ndarray :
        # we redraw the entire image,
        # because any gene could have been mutated
        blank_image = np.zeros_like( self.target_image )
        blank_image.fill( 255 )
        hsv_image = cv2.cvtColor( blank_image, cv2.COLOR_RGB2HSV )
        for circle in specimen.genes:
            gal.draw_circle_on_image( circle, hsv_image )
        return hsv_image
