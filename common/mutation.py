import random

from common.genetic_algorithm_interface import Population

def mutate_specimen_inplace(
        specimen,
        weighted_gene_mutation_functions,
        f_new_gene,
        p_add,
        p_del,
        p_id = None,
        mutation_rate = 0.2,
) -> None:

    mutation_weights = list( m[ 0 ] for m in weighted_gene_mutation_functions )
    mutation_functions = list( m[ 1 ] for m in weighted_gene_mutation_functions )

    _p_id = p_id or 1 - (p_add + p_del)
    weights = [ p_add * 100, p_del * 100, _p_id * 100 ]

    if len( specimen.genes ) >= 1:
        action_index = random.choices( [ 0, 1, 2 ], weights = weights )[ 0 ]
        if action_index == 0 :
            specimen.genes.append( f_new_gene() )
        elif action_index == 1 :
            deletion_index = int( random.random() * len( specimen.genes ) )
            del specimen.genes[ deletion_index ]
        else:
            pass # no gene is added or removed

    n_mutated_genes = int( mutation_rate * len( specimen.genes ) )
    mutation_indices = random.sample( range( len( specimen.genes ) ), k = n_mutated_genes )

    for i in mutation_indices:
        chosen_mutation = random.choices( mutation_functions, weights = mutation_weights )[ 0 ]
        chosen_mutation( specimen.genes[i] )


def random_shift_within_range( value, max_shift, range_min, range_max ):
    min_candidate = max( range_min, value - max_shift )
    max_candidate = min( range_max, value + max_shift )
    new_value = random.uniform( min_candidate, max_candidate )
    return new_value