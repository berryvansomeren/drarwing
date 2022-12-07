import random
from typing import Tuple, Union

from genetic_algorithms.common.genetic_algorithm_protocol import Image
from utils.random_shift_within_range import random_shift_within_range

import cv2
import numpy as np


BGRColor = Tuple[ int, int, int ]
HSVColor = Tuple[ int, int, int ]
Color = Union[ BGRColor, HSVColor ]


def random_hsv_color():
    random_h = random_color_hue()
    random_s = random_color_saturation()
    random_v = random_color_value()
    hsv_color = ( random_h, random_s, random_v )
    return hsv_color


# The function for random hue, saturation, value,
# might be useful in the future
# if you want to do more fine-grained mutations


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
    new_color = (
        # hue is cyclical so we use modulus
        int(random.uniform( color[0] - max_shift, color[0] + max_shift ) % 180),
        color[1],
        color[2]
    )
    return new_color


def random_shift_color_saturation( color : HSVColor, max_shift ) -> HSVColor:
    new_color = (
        color[0],
        int(random_shift_within_range( color[1], max_shift, 0, 255 )),
        color[2]
    )
    return new_color


def random_shift_color_value( color : HSVColor, max_shift ) -> HSVColor:
    new_color = (
        color[0],
        color[1],
        int(random_shift_within_range( color[2], max_shift, 0, 255 ))
    )
    return new_color


def get_blank_image_like( example_image, use_hsv = False ) -> Image:
    blank_image = np.zeros_like( example_image )
    blank_image.fill( 255 )
    if use_hsv:
        blank_image = cv2.cvtColor( blank_image, cv2.COLOR_BGR2HSV )
    return blank_image
