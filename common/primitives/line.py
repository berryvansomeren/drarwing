from dataclasses import dataclass
import random

import common.primitives.point as vgap_point


@dataclass
class Line :
    p1: vgap_point.Point
    p2: vgap_point.Point


def random_line( width : int, height : int ) -> Line:
    return Line( vgap_point.random_point( width, height ), vgap_point.random_point( width, height ) )


def line_translation( l : Line, options_x, options_y, width, height ) -> Line:

    def get_random_point_translation_options( p ):
        return vgap_point.get_random_point_translation_options( p, options_x, options_y, width, height )

    valid_options_x_1, valid_options_y_1 = get_random_point_translation_options( l.p1 )
    valid_options_x_2, valid_options_y_2 = get_random_point_translation_options( l.p2 )

    valid_options_x = list( set( valid_options_x_1 ) & set( valid_options_x_2 ) )
    valid_options_y = list( set( valid_options_y_1 ) & set( valid_options_y_2 ) )

    translation_x = random.choice( valid_options_x ) if valid_options_x else 0
    translation_y = random.choice( valid_options_y ) if valid_options_y else 0

    return Line(
        vgap_point.Point( l.p1.x + translation_x, l.p1.y + translation_y ),
        vgap_point.Point( l.p2.x + translation_x, l.p2.y + translation_y )
    )


def randomly_shift_one_point_of_line( l : Line, options_x, options_y, width, height ) -> Line:
    def point_translation( p ):
        return vgap_point.point_translation( p, options_x, options_y, width, height )

    p_index = random.choice([ 0, 1 ])
    if p_index == 0:
        return Line( point_translation( l.p1 ), l.p2 )
    else:
        return Line( l.p1, point_translation( l.p2 ) )
