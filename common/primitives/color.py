import copy
from dataclasses import dataclass
import random
from typing import Tuple

from common.mutation import random_shift_within_range


RGBColor = Tuple[ int, int, int ]


@dataclass
class HSVColor:
    hue         : int
    saturation  : int
    value       : int


rgb_color_black = ( 0, 0, 0 )
rgb_color_white = ( 255, 255, 255 )
rgb_color_grey  = ( 200, 200, 200 )
rgb_color_blue  = ( 203, 109, 44  )


def random_color():
    random_h = random_color_hue()
    random_s = random_color_saturation()
    random_v = random_color_value()
    hsv_color = HSVColor( random_h, random_s, random_v )
    # hsv_color = np.array( [ random_h, random_s, random_v ], dtype = 'uint8' ).reshape( 1, 1, 3 )
    # rgb_color = cv2.cvtColor( hsv_color, cv2.COLOR_HSV2RGB )
    return hsv_color


def random_color_hue() -> int:
    random_h = int( random.random() * 179 )
    return random_h

def random_color_saturation() -> int:
    random_s = int( random.random() * 255 )
    return random_s

def random_color_value() -> int:
    random_v = int( random.random() * 255 )
    return random_v


def random_shift_color_hue( color : HSVColor, max_shift ) -> HSVColor:
    new_color = copy.deepcopy( color )
    # hue is cyclical so we use modulus
    new_color.hue = random.uniform( color.hue - max_shift, color.hue + max_shift ) % 180
    return new_color

def random_shift_color_saturation( color : HSVColor, max_shift ) -> HSVColor:
    new_color = copy.deepcopy( color )
    new_color.saturation = random_shift_within_range( color.saturation, max_shift, 0, 255 )
    return new_color

def random_shift_color_value( color : HSVColor, max_shift ) -> HSVColor:
    new_color = copy.deepcopy( color )
    new_color.value = random_shift_within_range( color.value, max_shift, 0, 255 )
    return new_color

