import copy
from dataclasses import dataclass
import math
from typing import List, Optional, Tuple

import cv2
import numpy as np

import common


@dataclass
class Specimen:
    cached_image: np.ndarray
    diff_image: np.ndarray


Population = List[ Specimen ]


class Ellipsilly:

    target_image : Optional[ np.ndarray ]

    _n_population = 1

    _width : int
    _height : int
    _channels : int
    _min_radius : float
    _max_radius : float

    _select_n = 1

    _new_gene = None


    def __init__( self, target_image_rgb ):
        self.target_image = target_image_rgb
        self.dx, self.dy = common.get_image_gradients_from_hsv(self.target_image)
        self._height, self._width, self._channels = self.target_image.shape

        scharr_image = np.sqrt(self.dx**2 + self.dy**2)
        scharr_image = (scharr_image * 255/np.max(scharr_image)).astype(np.uint8)
        cv2.imwrite( f'C:/Users/Berry/Documents/development/visual_genetic_algorithms_playground/scharr.png', scharr_image )

        dx_image = (self.dx * 255/np.max(self.dx)).astype(np.uint8)
        cv2.imwrite( f'C:/Users/Berry/Documents/development/visual_genetic_algorithms_playground/dx.png', dx_image )

        dy_image = (self.dy * 255 / np.max( self.dy )).astype( np.uint8 )
        cv2.imwrite( f'C:/Users/Berry/Documents/development/visual_genetic_algorithms_playground/dy.png', dy_image )
        return

    def sample_new_ellipse( self, diff_image ):
        position = common.sample_weighted_position_from_image( diff_image )
        color = common.HSVColor(*(int( i ) for i in self.target_image[ position.y ][ position.x ]) )
        axes = (
            max( 5, int( math.sqrt(common.get_magnitude_from_gradients( self.dx, self.dy, position.x, position.y )) ) ),
            5
        )
        angle = math.degrees( common.get_direction_from_gradients( self.dx, self.dy, position.x, position.y ) ) + 90

        return common.Ellipse(
            color = color,
            position = position,
            axes = axes,
            angle = angle,
        )

    def get_initial_population( self ) -> Population:
        max_prob_image = np.ones( self.target_image.shape[ :2 ] )
        # we initialize the image once
        # and iterate by drawing on top of those images
        blank_image = np.zeros_like( self.target_image )
        blank_image.fill( 255 )

        initial_population = [
            Specimen(copy.deepcopy(blank_image), max_prob_image)
            for _ in range( self._n_population )
        ]
        return initial_population

    def apply_crossover( self, population : Population ) -> Population:
        return common.simple_copy_padding(population, self._n_population)

    def apply_mutation_inplace( self, population : Population ):
        for specimen in population:
            new_ellipse = self.sample_new_ellipse( specimen.diff_image )
            common.draw_ellipse_on_image( new_ellipse, specimen.cached_image )

    def get_fitness( self, population : Population ) -> common.FitnessScores:
        population_fitnesses = [ ]
        for specimen in population :
            specimen_image = self.draw_specimen( specimen )
            absolute_difference_image = common.get_absolute_difference_image( specimen_image, self.target_image )
            specimen.diff_image = absolute_difference_image
            fitness = common.get_fitness_from_absolute_difference_image( absolute_difference_image )
            population_fitnesses.append( fitness )
        return population_fitnesses

    def apply_selection( self, population: Population, fitness_scores: common.FitnessScores ) -> Tuple[ Population, common.FitnessScores ] :
        return common.select_top_n(population, fitness_scores, self._select_n)

    def draw_specimen( self, specimen: Specimen ) -> np.ndarray :
        # we already have drawn it during mutation!
        return specimen.cached_image

    def get_specimen_image( self, specimen: Specimen ) -> np.ndarray:
        return specimen.cached_image
