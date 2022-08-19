from typing import List, Tuple

from common.genetic_algorithm_interface import Population, FitnessScores


def select_top_n( population : List, fitness_scores : FitnessScores, n : int ) -> Tuple[ Population, FitnessScores ]:
    population_sorted, fitness_scores_sorted = zip(
        *sorted(
            zip( population, fitness_scores ),
            key = lambda t : t[ 1 ]
        )
    )
    selected_population = list( population_sorted )[ :n ]
    selected_fitness_scores = list( fitness_scores_sorted )[ :n ]
    return selected_population, selected_fitness_scores


def select_with_rate( population : List, fitness_scores : FitnessScores, selection_rate ):
    n_select = max( 1, int( selection_rate * len( population ) ) )
    return select_top_n( population, fitness_scores, n_select )
