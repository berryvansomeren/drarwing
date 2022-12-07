import random

from genetic_algorithms.common.genetic_algorithm_protocol import GeneticAlgorithm
from typing import Generator

import numpy as np


def make_genetic_algorithm_generator( genetic_algorithm : GeneticAlgorithm, random_seed : int = 1337 ) -> Generator:
    """
    A generator that for every iteration of the genetic algorithm returns results
    """
    # use a seed to make things reproducible
    random.seed( random_seed )
    np.random.seed( random_seed )

    generation_index = 0
    parent_population = genetic_algorithm.get_initial_population()

    while not genetic_algorithm.is_done():
        generation_index += 1

        # Note that performing reproduction for the first time,
        # might not result in any offspring.
        population = genetic_algorithm.apply_reproduction( parent_population )
        genetic_algorithm.apply_mutation_inplace( population )

        # add non-mutated parents back to population,
        # to guarantee that fitness scores will never become worse
        population += parent_population

        fitness_scores = genetic_algorithm.get_fitness( population )
        selected_population, selected_fitness_scores = genetic_algorithm.apply_selection(
            population,
            fitness_scores,
        )

        # Sort population on fitness
        # Lower fitness score is better!
        scored_population = zip( selected_population, selected_fitness_scores )
        get_fitness = lambda t : t[ 1 ]
        population_sorted, fitness_scores_sorted = zip( *sorted( scored_population, key = get_fitness ) )
        best_specimen = population_sorted[0]

        # This population will be the parents of the next generation
        parent_population = list(population_sorted)

        best_image = genetic_algorithm.get_specimen_image_rgb(best_specimen)
        best_score = fitness_scores_sorted[0]

        yield generation_index, best_image, best_score, best_specimen
