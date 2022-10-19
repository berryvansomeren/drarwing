from dataclasses import dataclass, astuple

import cv2
import numpy as np

from common.primitives.color import HSVColor
from common.primitives.point import Point


@dataclass
class Circle:
    color       : HSVColor
    position    : Point
    radius      : float


def draw_circle_on_image( circle : Circle, image : np.ndarray ) -> np.ndarray:
    image = cv2.circle( image,
        center = astuple( circle.position ),
        radius = circle.radius,
        color = circle.color,
        thickness = cv2.FILLED,
        lineType = cv2.LINE_AA
    )
    return image