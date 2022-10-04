from pathlib import Path
import random
from typing import List, Optional, Tuple, TypeVar, Generator
from abc import ABC, abstractmethod

import numpy as np


FitnessScore    = float
FitnessScores   = List[FitnessScore]
Specimen        = TypeVar('Specimen') # Genetic algorithms mainly differ in how their Specimen are defined
Population      = List[Specimen]


# The protocol for a genetic_algorithm is not super strict,
# The two functions under this class define ways to deal with optional methods the protocol could implement
class GeneticAlgorithm(ABC):
    @abstractmethod
    def get_initial_population( self ) -> Population :
        pass

    @abstractmethod
    def apply_crossover( self, population ) -> Population:
        """
        Note that currently the parent populations is always added back to the population after crossover.
        This is to guarantee that fitness scores will never become worse after crossover.
        Even if all mutations are bad, the same parents will be selected again,
        and the best score for the generation will be equal to that of the last
        """
        pass

    @abstractmethod
    def apply_mutation_inplace( self, population ) -> None:
        pass

    @abstractmethod
    def get_fitness( self, population: Population ) -> FitnessScores:
        """
        Note that throughout this program it is assumed that lower fitness scores are better.
        Scores are commonly an equality percentage between result and target
        """
        pass

    @abstractmethod
    def apply_selection( self, population, fitness_scores ) -> Tuple[ Population, FitnessScores ]:
        pass

    @abstractmethod
    def get_specimen_image_rgb( self, specimen: Specimen ) -> np.ndarray:
        """
        You might want to use a different color space in your genetic algorithm,
        but this function should always return an RGB image.
        Try to do as few color space transformations as necessary to keep the code fast.
        """
        pass

    def is_done( self ) -> bool:
        # by default a genetic algorithm will run indefinitely
        return False


def make_genetic_algorithm_generator( genetic_algorithm : GeneticAlgorithm, random_seed : int = 1337 ) -> Generator:
    """
    A generator that for every iteration of the genetic algorithm returns results
    """
    # use seed to make things reproducible
    random.seed( random_seed )

    generation_index = 0
    parent_population = genetic_algorithm.get_initial_population()

    while not genetic_algorithm.is_done():
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
        best_specimen = population_sorted[0]

        parent_population = list(population_sorted)

        best_image = genetic_algorithm.get_specimen_image_rgb(best_specimen)
        best_score = fitness_scores_sorted[0]

        yield generation_index, best_image, best_score, best_specimen
