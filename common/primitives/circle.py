from dataclasses import dataclass, astuple
import random

import cv2
import numpy as np

from common.primitives.color import HSVColor, random_hsv_color
from common.primitives.point import Point, random_point


@dataclass
class Circle:
    color       : HSVColor
    position    : Point
    radius      : float


def random_circle_radius( min_radius, max_radius ):
    return random.randint( min_radius, max_radius )


def random_circle( width, height, min_radius, max_radius ):
    circle = Circle(
        color       = random_hsv_color(),
        position    = random_point( width, height ),
        radius      = random_circle_radius( min_radius, max_radius )
    )
    return circle


def draw_circle_on_image( circle : Circle, image : np.ndarray ) -> np.ndarray:
    image = cv2.circle( image,
        center = astuple( circle.position ),
        radius = circle.radius,
        color = circle.color,
        thickness = -1,
        lineType = cv2.LINE_AA
    )
    return image