import numpy as np

from genetic_algorithms.common.genetic_algorithm_protocol import FitnessScore
from utils.absolute_difference_image import get_absolute_difference_image


def get_fitness_as_absolute_image_difference( specimen_image, target_image ) -> FitnessScore:
    absolute_difference_image = get_absolute_difference_image( specimen_image, target_image )
    fitness = get_fitness_from_absolute_difference_image( absolute_difference_image )
    return fitness


def get_fitness_from_absolute_difference_image( absolute_difference_image ) -> FitnessScore:
    image_score = float( np.sum( absolute_difference_image ) )
    n_elements = np.prod( absolute_difference_image.shape )
    max_potential_diff_score = n_elements * 255
    normalized_diff_score = image_score / max_potential_diff_score
    return normalized_diff_score
