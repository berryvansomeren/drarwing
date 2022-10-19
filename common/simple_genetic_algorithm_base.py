from typing import Tuple
from abc import ABC, abstractmethod

from common.reproduction import asexual_copy_reproduction
from common.fitness import get_absolute_difference_image, get_fitness_from_absolute_difference_image
from common.selection import select_top_n

from common.genetic_algorithm_protocol import (
    Specimen,
    Population,
    FitnessScores,
    Image,
)


class SimpleGeneticAlgorithmBase( ABC ):

    """
    This Abstract base class defines default implementations for many of the GeneticAlgorithm methods.
    Conceptually I do not think they are typical default implementation for genetic algorithms in general,
    but they turned out to be useful defaults for the genetic algorithms I created.

    Note that an argument could be made that as a genetic algorithm this is very minimal,
    because the reproduction is asexual and there is no crossover of genes from different parents,
    and survival of the fittest boils down to whether the last mutation was an improvement or not,
    because n_selection is also 1 by default.
    This could have been written as a big for loop,
    but the benefit of a genetic/evolutionary setup is that you can easily experiment with many cool variations!
    """

    def __init__( self, target_image : Image, n_population : int = 1, n_selection : int = 1 ):
        self._target_image = target_image
        self._n_population = n_population
        self._n_selection = n_selection
        self._height, self._width, self._channels = self._target_image.shape

    @abstractmethod
    def get_initial_population( self ) -> Population :
        """
        How to initialize the population depends very much on the concrete implementation of Specimen
        """
        pass

    @abstractmethod
    def apply_mutation_inplace( self, population : Population ) -> None:
        """
        How to mutate the population depends very much on the concrete implementation of Specimen
        The mutation functions used, shape the whole identity of the genetic algorithm
        """
        pass

    def apply_reproduction( self, population : Population ) -> Population:
        """
        Note that currently the parent populations is always added back to the population after mutations.
        This is to guarantee the best fitness score of the population will never become worse.
        Even if all mutations are bad, the same parents will be selected again,
        and the best score for the generation will be equal to that of the previous.
        """
        return asexual_copy_reproduction( population, self._n_population )

    def get_fitness( self, population: Population ) -> FitnessScores:
        """
        Note that throughout this project it is assumed that lower fitness scores are better.
        Scores are commonly a percentage, measuring equality between result and target
        """
        population_fitnesses = [ ]
        for specimen in population :
            absolute_difference_image = get_absolute_difference_image( specimen.cached_image, self._target_image )
            specimen.diff_image = absolute_difference_image
            fitness = get_fitness_from_absolute_difference_image( absolute_difference_image )
            population_fitnesses.append( fitness )
        return population_fitnesses

    def apply_selection( self, population : Population, fitness_scores : FitnessScores ) -> Tuple[ Population, FitnessScores ]:
        """
        Selection is very simple: take the specimen with the top N fitness scores
        """
        return select_top_n(population, fitness_scores, self._n_selection)

    def get_specimen_image_rgb( self, specimen: Specimen ) -> Image:
        """
        You might want to use a different color space in your genetic algorithm,
        but this function should always return an RGB image.
        If your algorithm internally uses a different color space,
        you'll have to override this method and do a color space transformation.
        Try to do as few color space transformations as necessary to keep the code fast.
        """
        return specimen.cached_image

    def is_done( self ) -> bool:
        # By default, a genetic algorithm itself wants to run indefinitely
        # However, the code that runs the genetic algorithm might impose additional termination criteria
        return False

