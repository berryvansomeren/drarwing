import copy
from dataclasses import dataclass, field
import math
from pathlib import Path
from typing import List

from genetic_algorithms.common.genetic_algorithm_protocol import Image, Population, FitnessScores
from genetic_algorithms.common.simple_genetic_algorithm_base import SimpleGeneticAlgorithmBase
from primitives.brush import Brush, preload_brush_textures, draw_brush_on_image, random_brush_texture_index
from utils.image_gradient import ImageGradient

class Painting( SimpleGeneticAlgorithmBase ):

    """
    Iterative Painting

    We improve a painting iteratively by adding more brush strokes.
    The position of a brush stroke is affected by the difference with the target image
    The color of a brush stroke is determined by the color of the target image at that position
    The orientation of the brush stroke is affected by the gradient of the target image in that position
    The size of the brush stroke is based on the fitness score, which measures the difference with the target image.
    When the difference becomes smaller, brush strokes will become smaller.
    """

    @dataclass
    class Specimen :
        cached_image: Image
        diff_image: Image

        # We normally do not store fitness scores inside the specimen
        # But we do for this algorithm,
        # because the score is used to determine brush size
        fitness : float

        # The brushes are basically the genes of the specimen.
        # We do not actually use them in the algorithm,
        # because we can directly draw changes on top of the cached image
        # But storing this info allows for better inspection,
        # and to later redraw the image with different settings, if pickled.
        # For that, see common.redraw.redraw_painting
        brushes: List[ Brush ] = field( default_factory = list )


    def __init__(
            self,
            target_image    : Image,
            brush_directory     : str,

            # these are fun to play around with
            # configure the size multiplier to get more coarse or finegrained results
            # Note that it will affect convergence speed
            size_multiplier     : int = 1,
            min_brush_size      : int = 10,
    ):
        super().__init__( target_image )

        self.target_gradient = ImageGradient( self._target_image )
        preload_brush_textures( Path( brush_directory ) )

        self.brush_size_multiplier = size_multiplier
        self.min_brush_size = min_brush_size

    def get_initial_population( self ) -> Population:
        blank_image = GA_common.get_blank_image_like( self._target_image )
        abs_diff_image = GA_common.get_absolute_difference_image( blank_image, self._target_image )
        fitness = GA_common.get_fitness_from_absolute_difference_image( abs_diff_image )
        initial_population = [
            self.Specimen(
                cached_image = copy.deepcopy( blank_image ),
                diff_image = abs_diff_image,
                fitness = fitness
            )
            for _ in range( self._n_population )
        ]
        return initial_population

    def _get_brush_size( self, specimen_fitness ):
        # Note that the fitness score is actually the percentage of difference with the target image
        # The brush size is then simply a percentage of the size of the image, based on this difference,
        # and scaled with a configurable parameter.
        image_min_extend = min( self._height, self._width )
        scaled_brush_size = int( image_min_extend * specimen_fitness ) * self.brush_size_multiplier
        brush_size = max( self.min_brush_size, scaled_brush_size )
        return brush_size

    def apply_mutation_inplace( self, population : Population ):
        for specimen in population:
            position = GA_common.sample_weighted_position_from_image( specimen.diff_image )
            color = GA_common.get_color_from_image( self._target_image, position )
            texture_index = GA_common.random_brush_texture_index()
            angle = math.degrees( self.target_gradient.get_direction( position ) )
            brush_size = self._get_brush_size(specimen.fitness)
            new_brush = Brush(
                color = color,
                position = position,
                texture_index = texture_index,
                angle = angle,
                size = brush_size,
            )
            draw_brush_on_image( new_brush, specimen.cached_image )
            specimen.brushes.append( new_brush )

    def get_fitness( self, population : Population ) -> FitnessScores:
        # we are caching the best fitness score as we use it for brush size calculation if autoscaling is True
        population_fitnesses = super().get_fitness( population )
        # cache the fitness scores per specimen as we will use them to determine new brush sizes
        for specimen, fitness in zip(population, population_fitnesses ):
            specimen.fitness = fitness
        return population_fitnesses


def get(target_image, **kwargs):
    return Painting(target_image, **kwargs)
