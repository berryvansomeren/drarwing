import random


def random_shift_within_range( value, max_shift, range_min, range_max ):
    min_candidate = max( range_min, value - max_shift )
    max_candidate = min( range_max, value + max_shift )
    new_value = random.uniform( min_candidate, max_candidate )
    return new_value