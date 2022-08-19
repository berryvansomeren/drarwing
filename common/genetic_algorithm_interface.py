from pathlib import Path
import random
from typing import Any, List, Optional, Tuple, TypeVar, Generator, Protocol

import numpy as np


FitnessScore    = float
FitnessScores   = List[FitnessScore]
Specimen        = TypeVar('Specimen')
Population      = TypeVar('Population')


# A generic object to store debug info
# Needs to be provided with a path in order to write debug output to disk
class DebugInfo(Protocol):
    def write( self, output_folder : Path ):
        pass


# The protocol for a genetic_algorithm is not super strict,
# The two functions under this class define ways to deal with optional methods the protocol could implement
class GeneticAlgorithm(Protocol):
    def apply_crossover( self, population ) -> Population:
        """
        Note that currently the parent populations is always added back to the population after crossover.
        This is to guarantee that fitness scores will never become worse after crossover.
        Even if all mutations are bad, the same parents will be selected again,
        and the best score for the generation will be equal to that of the last
        """
        pass

    def apply_mutation_inplace( self, population ) -> None:
        pass

    def get_fitness( self, population: Population ) -> FitnessScores:
        """
        Note that throughout this program it is assumed that lower fitness scores are better.
        Scores are commonly an equality percentage between result and target
        """
        pass

    def apply_selection( self, population, fitness_scores ) -> Tuple[ Population, FitnessScores ]:
        pass

    def draw_specimen_rgb( self, specimen: Specimen ) -> np.ndarray:
        """
        You might want to use a different color space in your genetic algorithm,
        but this function should always return an RGB image.
        Try to do as few color space transformations as necessary to keep the code fast.
        """
        pass

    # Optional:
    # def is_done( self ) -> bool:
    #     pass

    # Optional:
    # def get_debug_info( self ) -> DebugInfo:
    #     pass


def _is_done( genetic_algorithm ) -> Any:
    # if the genetic algorithm can tell is when it is done, listen to it
    # if it can not tell us, just iterate indefinitely until we finally run out of patience
    f_or_none = getattr( genetic_algorithm, 'is_done', None )
    return f_or_none( genetic_algorithm ) if f_or_none else False


def _get_debug_info( genetic_algorithm ) -> Optional[ DebugInfo ]:
    f_or_none = getattr( genetic_algorithm, 'get_debug_info', None )
    return f_or_none( genetic_algorithm ) if f_or_none else None


def make_genetic_algorithm_generator_class( genetic_algorithm, random_seed : int = 1337 ) -> Generator:
    """
    A generator that for every iteration of the genetic algorithm returns the fitness scores and population
    Note: the return scores and population are not sorted!
    """
    # seed to make things reproducible
    random.seed( random_seed )

    generation_index = 0
    parent_population = genetic_algorithm.get_initial_population()

    while not _is_done(genetic_algorithm):
        generation_index += 1
        population = genetic_algorithm.apply_crossover( parent_population )
        genetic_algorithm.apply_mutation_inplace( population )

        # add unmutated parents back to population,
        # to guarantee that fitness scores will never become worse
        population += parent_population

        fitness_scores = genetic_algorithm.get_fitness( population )
        selected_population, selected_fitness_scores = genetic_algorithm.apply_selection(
            population,
            fitness_scores,
        )

        # Sort population of fitness
        # Lower fitness score is better!
        scored_population = zip( selected_population, selected_fitness_scores )
        get_fitness = lambda t : t[ 1 ]
        population_sorted, fitness_scores_sorted = zip( *sorted( scored_population, key = get_fitness ) )
        parent_population = list(population_sorted)

        best_image = genetic_algorithm.draw_specimen( parent_population[0] )
        best_score = fitness_scores_sorted[0]
        debug_info = _get_debug_info( genetic_algorithm )

        yield generation_index, best_image, best_score, debug_info
