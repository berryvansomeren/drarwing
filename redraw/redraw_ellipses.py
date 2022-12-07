import math

import numpy as np

from primitives import Image, Point
from primitives.ellipse import Ellipse, draw_ellipse_on_image_as_bgr
from redraw.utils import get_scale_for_4k_from_image
from genetic_algorithms.impl.pointillism import Pointillism


def _redraw_ellipses(
        ellipses : list[Ellipse],
        scale: float,
        result_image: np.ndarray,
) -> Image:

    def int_scale(v):
        return int( v * scale )

    for ellipse in ellipses:
        ellipse.size = ( int_scale(ellipse.axes[0]), int_scale(ellipse.axes[1]) )
        ellipse.position = Point(
            int_scale(ellipse.position.x),
            int_scale(ellipse.position.y),
        )
        draw_ellipse_on_image_as_bgr( ellipse, result_image )

    return result_image


def redraw_pointillism_at_4k(
        specimen : Pointillism.Specimen
):
    scale = get_scale_for_4k_from_image( specimen.cached_image )

    result_image_shape = (
        math.ceil( specimen.cached_image.shape[0] * scale ),
        math.ceil( specimen.cached_image.shape[1] * scale ),
        3
    )
    result_image = np.zeros( result_image_shape, dtype = np.uint8 )
    result_image.fill(255)

    result = _redraw_ellipses(
        specimen.genes,
        scale,
        result_image
    )

    return result
