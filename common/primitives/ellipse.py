from dataclasses import dataclass, astuple
import random
from typing import Tuple

import cv2
import numpy as np

from common.primitives.color import Color
from common.primitives.point import Point, random_point


@dataclass
class Ellipse:
    color       : Color
    position    : Point
    axes        : Tuple[ int, int ]
    angle       : float


def draw_ellipse_on_image( ellipse : Ellipse, image : np.ndarray ) -> np.ndarray:
    image = cv2.ellipse( image,
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