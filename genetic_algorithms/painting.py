import copy
from dataclasses import dataclass, field
import logging
import math
from pathlib import Path
from typing import List, Tuple

import numpy as np

import common


@dataclass
class Specimen:
    cached_image: np.ndarray
    diff_image: np.ndarray

    # The brushes are basically the "genes" of the specimen.
    # We do not actually use them in the algorithm,
    # because we can directly draw changes on top of the cached image
    # But storing this info allows for better inspection,
    # and to later redraw the image with different settings
    # For that, see utils/redraw_painting.py
    brushes: List[ common.Brush ] = field(default_factory=list)


Population = List[ Specimen ]


class Painting(common.GeneticAlgorithm):

    """
    Iterative Painting

    We improve a painting iteratively by adding more brush strokes.
    The position of a brush stroke is affected by the difference with the target image
    The color of a brush stroke is determined by the color of the target image at that position
    The orientation of the brush stroke is affected by the gradient of the target image in that position
    The size of the brush stroke is based on the fitness score, which measures the difference with the target image.
    When the difference becomes smaller, brush strokes will become smaller.

    Note that as a genetic algorithm this does not really count,
    because the population size is 1 by default, there is no crossover,
    and survival of the fittest boils down to whether the last mutation was an improvement or not.
    This could have been written as a big for loop,
    but the benefit of a genetic/evolutionary setup is that you can easily experiment with many cool variations!
    """

    def __init__(
            self,
            target_image_rgb    : np.ndarray,
            brush_directory     : str,

            # these are fun to play around with
            # configure the size multiplier to get more coarse or finegrained results
            # Note that it will affect convergence speed
            size_multiplier     : int = 1,
            min_brush_size      : int = 10,

            # these are not really recommended to change
            n_population:   int = 1,
            select_n:       int = 1,

            autoscaling_brush_size  = True,
            fixed_brush_size        = None
    ):
        self._target_image = target_image_rgb
        self.dx, self.dy = common.get_image_gradients_from_hsv( self._target_image )
        self._height, self._width, self._channels = self._target_image.shape

        common.preload_brush_textures( Path(brush_directory) )

        self.autoscaling_brush_size = autoscaling_brush_size
        if self.autoscaling_brush_size:
            if fixed_brush_size is not None:
                logging.error('Since autoscaling_brush_size is True, we do not expect a fixed_brush_size to be passed.')
            self.brush_size_multiplier = size_multiplier
            self.min_brush_size = min_brush_size
        else:
            if fixed_brush_size is None:
                logging.error('Since autoscaling_brush_size is False, we do expect a fixed_brush_size to be passed.' )
            self.fixed_brush_size = fixed_brush_size

        self._n_population = n_population
        self._select_n = select_n

        # this is used to calculate brush size
        self._last_best_fitness = 1.0

    def get_initial_population( self ) -> Population:
        # We start off with a blank canvas
        max_prob_image = np.ones( self._target_image.shape[ :2 ] )
        blank_image = np.zeros_like( self._target_image )
        blank_image.fill(255)

        initial_population = [
            Specimen(copy.deepcopy(blank_image), max_prob_image)
            for _ in range( self._n_population )
        ]
        return initial_population

    def apply_crossover( self, population : Population ) -> Population:
        # In case the population size equals 1 (which it is by default), this does nothing
        return common.simple_copy_padding(population, self._n_population)

    def _get_brush_size( self ):
        if self.autoscaling_brush_size:
            # Note that the fitness score is actually the percentage of difference with the target image
            # The brush size is then simply a percentage of the size of the image, based on this difference,
            # and scaled with a configurable parameter.
            image_min_extend = min( self._height, self._width )
            scaled_brush_size = int( image_min_extend * self._last_best_fitness ) * self.brush_size_multiplier
            brush_size = max( self.min_brush_size, scaled_brush_size )
            return brush_size
        else:
            return self.fixed_brush_size

    def apply_mutation_inplace( self, population : Population ):
        for specimen in population:
            position = common.sample_weighted_position_from_image( specimen.diff_image )
            color = self._target_image[ position.y ][ position.x ]
            texture_index = common.random_brush_texture_index()
            angle = math.degrees( common.get_direction_from_gradients( self.dx, self.dy, position.x, position.y ) )
            brush_size = self._get_brush_size()
            new_brush = common.Brush(
                color = color,
                position = position,
                texture_index = texture_index,
                angle = angle,
                size = brush_size,
            )
            common.draw_brush_on_image(new_brush, specimen.cached_image)
            specimen.brushes.append(new_brush)

    def get_fitness( self, population : Population ) -> common.FitnessScores:
        # Note that the fitness score is actually the percentage of difference with the target image
        population_fitnesses = [ ]
        for specimen in population :
            absolute_difference_image = common.get_absolute_difference_image( specimen.cached_image, self._target_image )
            specimen.diff_image = absolute_difference_image
            fitness = common.get_fitness_from_absolute_difference_image( absolute_difference_image )
            population_fitnesses.append( fitness )

        # caching the best fitness score as we use it for brush size calculation if autoscaling is True
        self._last_best_fitness = min(population_fitnesses)
        return population_fitnesses

    def apply_selection( self, population: Population, fitness_scores: common.FitnessScores ) -> Tuple[ Population, common.FitnessScores ] :
        return common.select_top_n(population, fitness_scores, self._select_n)

    def get_specimen_image_rgb( self, specimen: Specimen ) -> np.ndarray:
        # we don't have to do anything exceptional here,
        # because the whole algorithm has been using RGB color space the whole time,
        # and the result image is already cached
        # Those things might not necessarily be true for other genetic algorithms in this project
        return specimen.cached_image


def get(target_image, **kwargs):
    return Painting(target_image, **kwargs)
