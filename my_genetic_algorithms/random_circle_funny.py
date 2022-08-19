import copy
from dataclasses import dataclass
from typing import List, Optional, Tuple

import cv2
import numpy as np

import common as gal


@dataclass
class Specimen:
    cached_image: np.ndarray
    genes: List[ gal.Circle ]

Population = List[ Specimen ]


class GeneticCircleDrawing:

    target_image : Optional[ np.ndarray ]

    _n_population = 1

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

    def sample_new_circle( self ):
        return gal.random_circle(
            self._width,
            self._height,
            self._min_radius,
            self._max_radius
        )

    def get_initial_population( self ) -> Population:
        # we initialize the image once
        # and iterate by drawing on top of those images
        blank_image = np.zeros_like( self.target_image )
        blank_image.fill( 255 )
        hsv_image = cv2.cvtColor( blank_image, cv2.COLOR_RGB2HSV )

        initial_population = [
            Specimen(
                copy.deepcopy(hsv_image),
                [self.sample_new_circle()]
            ) for _ in range( self._n_population )
        ]
        return initial_population

    def apply_crossover( self, population : Population ) -> Population:
        return population # do nothing...

    def apply_mutation_inplace( self, population : Population ):
        for specimen in population:
            specimen.genes.append(self.sample_new_circle())

    def get_fitness( self, population : Population ) -> gal.FitnessScores:
        return [
            gal.get_fitness_as_absolute_image_difference(
                specimen.cached_image,
                self.target_image
            )
            for specimen in population
        ]

    def apply_selection( self, population: Population, fitness_scores: gal.FitnessScores ) -> Tuple[ Population, gal.FitnessScores ] :
        return population, fitness_scores # Do nothing...

    def draw_specimen( self, specimen: Specimen ) -> np.ndarray :
        # every iteration adds exactly 1 gene,
        # and since we cached the result of previous iteration,
        # we only need to paint the last gene on top of the cached image
        gal.draw_circle_on_image( specimen.genes[-1], specimen.cached_image )
        return specimen.cached_image


def make_genetic_algorithm( target_image ):
    return GeneticCircleDrawing( target_image )
