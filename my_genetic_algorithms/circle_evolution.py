from dataclasses import dataclass
from typing import List, Optional, Tuple

import cv2
import numpy as np

import common as gal

@dataclass
class Specimen:
    genes: List[ gal.Circle ]

Population = List[ Specimen ]


class CircleEvolution:

    target_image : np.ndarray

    _n_population   = 100
    _n_genes        = 30
    _n_selection    = 5

    _width : int
    _height : int
    _channels : int

    _min_radius : float
    _max_radius : float

    def __init__( self, target_image_rgb ):
        self.target_image = cv2.cvtColor( target_image_rgb, cv2.COLOR_RGB2HSV )
        self._height, self._width, self._channels = self.target_image.shape
        self._min_radius = int( 0.05 * min(self._width, self._height) )
        self._max_radius = int( 0.15 * min(self._width, self._height) )

    def get_random_circle( self ):
        return gal.random_circle(
            self._width,
            self._height,
            self._min_radius,
            self._max_radius
        )

    def get_initial_population( self ) -> Population:
        initial_population = []
        for _ in range( self._n_population ):
            circles = [ ]
            for _ in range( self._n_genes ) :
                circles.append( self.get_random_circle() )
            initial_population.append( Specimen( circles ) )
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
        gal.mutate_specimens_inplace(
            population,
            weighted_mutations,
            self.get_random_circle,
            p_add = 0.2,
            p_del = 0.1,
        )


    def get_fitness( self, population : Population ) -> gal.FitnessScores:
        return [
            gal.get_fitness_as_absolute_image_difference(
                self.draw_specimen( specimen ),
                self.target_image
            )
            for specimen in population
        ]


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
