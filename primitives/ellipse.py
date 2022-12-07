from dataclasses import dataclass, astuple
from typing import Tuple

import cv2
import numpy as np

from primitives.color import Color, HSVColor
from primitives.point import Point


@dataclass
class Ellipse:
    color       : Color
    position    : Point
    axes        : Tuple[ int, int ]
    angle       : float


def draw_ellipse_on_image( ellipse : Ellipse, image : np.ndarray ) -> np.ndarray:
    image = cv2.ellipse(
        image,
        center = astuple( ellipse.position ),
        axes = ellipse.axes,
        angle = ellipse.angle,
        startAngle = 0,
        endAngle = 360,
        color = ellipse.color,
        thickness = cv2.FILLED,
        lineType = cv2.LINE_AA
    )
    return image


def draw_ellipse_on_image_as_bgr( ellipse : Ellipse, image : np.ndarray ) -> np.ndarray:

    draw_color = ellipse.color
    if isinstance(ellipse.color, HSVColor):
        draw_color = cv2.cvtColor( draw_color, cv2.COLOR_HSV2BGR )

    image = cv2.ellipse( image,
        center = astuple( ellipse.position ),
        axes = ellipse.axes,
        angle = ellipse.angle,
        startAngle = 0,
        endAngle = 360,
        color = draw_color,
        thickness = cv2.FILLED,
        lineType = cv2.LINE_AA
    )
    return image
