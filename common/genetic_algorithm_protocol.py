from typing import List, Tuple, TypeVar, Protocol
from abc import abstractmethod

import numpy as np


Specimen = TypeVar( 'Specimen' )
Population = List[ Specimen ]
FitnessScore = float
FitnessScores = List[ FitnessScore ]
Image = np.ndarray


class GeneticAlgorithm(Protocol):
    """
    This Protocol defines all function that are expected to exist,
    in order to use for example make_genetic_algorithm_generator
    """

    @abstractmethod
    def get_initial_population( self ) -> Population :
        pass

    @abstractmethod
    def apply_reproduction( self, population : Population ) -> Population:
        pass

    @abstractmethod
    def apply_mutation_inplace( self, population : Population ) -> None:
        pass

    @abstractmethod
    def get_fitness( self, population: Population ) -> FitnessScores:
        pass

    @abstractmethod
    def apply_selection( self, population : Population , fitness_scores : FitnessScores ) -> Tuple[ Population, FitnessScores ]:
        pass

    @abstractmethod
    def get_specimen_image_rgb( self, specimen: Specimen ) -> Image:
        pass

    @abstractmethod
    def is_done( self ) -> bool:
        pass
