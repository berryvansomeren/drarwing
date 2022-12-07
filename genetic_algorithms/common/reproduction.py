import copy
import random

from genetic_algorithms.common.genetic_algorithm_protocol import Population


def specimen_random_distribute_crossover( parent_1, parent_2 ):
    n_min_genes = min( len( parent_1 ), len( parent_2 ) )
    n_max_genes = max( len( parent_1 ), len( parent_2 ) )

    child_1 = [ ]
    child_2 = [ ]
    for gene_i in range( n_min_genes ) :
        chosen_order = random.randint( 0, 1 )
        if chosen_order == 0 :
            child_1.append( parent_1[ gene_i ] )
            child_2.append( parent_2[ gene_i ] )
        else :
            child_1.append( parent_2[ gene_i ] )
            child_2.append( parent_1[ gene_i ] )

    # distribute excess genes from the longer parent
    longer_parent = parent_1 if len( parent_1 ) > len( parent_2 ) else parent_2
    for i in range( n_max_genes - n_min_genes ) :
        gene_i = n_min_genes + i
        chosen_order = random.randint( 0, 1 )
        if chosen_order == 0 :
            child_1.append( longer_parent[ gene_i ] )
        else :
            child_2.append( longer_parent[ gene_i ] )

    return child_1, child_2


def random_list_crossover( population : Population ) -> Population:
    offspring = []
    # we create random pairs by randomly shuffling the population and iterating over consecutive pairs
    random.shuffle( population )
    for parent_1, parent_2 in zip( population[ 0::2 ], population[ 1::2 ] ) :
        children = specimen_random_distribute_crossover( parent_1, parent_2 )
        offspring += children

    assert len( offspring ) == len( population )
    return offspring


def asexual_copy_reproduction( parent_population, target_size ):
    n_copies, n_remainder = divmod( target_size, len(parent_population) )
    new_population = []
    for _ in range(n_copies):
        new_population.extend( copy.deepcopy(parent_population))
    new_population.extend( copy.deepcopy(parent_population[:n_remainder]))
    return new_population
