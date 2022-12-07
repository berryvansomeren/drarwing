import numpy as np

from primitives.color import Color
from primitives.point import Point


def get_color_from_image( image : np.ndarray, position : Point ) -> Color:
    color_raw = image[ position.y, position.x ]
    color = ( int(color_raw[0]), int(color_raw[1]), int(color_raw[2]) )
    return color
