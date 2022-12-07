from dataclasses import dataclass
import random

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, List

from primitives.color import Color
from primitives.point import Point


@dataclass
class Brush:
    color           : Color
    texture_index   : int
    position        : Point
    angle           : float
    size            : int


PRELOADED_BUSH_TEXTURES : Optional[List ] = None


def set_global_brush_textures( brush_textures : List[np.ndarray ] ) -> None:
    global PRELOADED_BUSH_TEXTURES
    PRELOADED_BUSH_TEXTURES = brush_textures


def get_global_brush_textures() -> List[np.ndarray]:
    return PRELOADED_BUSH_TEXTURES


def preload_brush_textures( directory_name : Path ):
    texture_paths = []
    for extension in [ '.jpg', '.png' ]:
        texture_paths.extend( list( directory_name.rglob( f'*{extension}' ) ) )
    textures = [ cv2.imread( str(texture_path) ) for texture_path in texture_paths ]
    textures = [ cv2.cvtColor( texture, cv2.COLOR_BGR2GRAY ) for texture in textures ]
    set_global_brush_textures( textures )


def random_brush_texture_index():
    return random.choice( range( len( get_global_brush_textures() ) ) )


def draw_brush_on_image( brush : Brush, image : np.ndarray ) -> np.ndarray:
    image_height, image_width = image.shape[:2]

    brush_texture_original = get_global_brush_textures()[brush.texture_index ]
    brush_texture_scaled = cv2.resize( brush_texture_original, (brush.size, brush.size) )
    brush_height, brush_width = brush_texture_scaled.shape[:2]

    transformation_matrix = cv2.getRotationMatrix2D( (brush_width/2, brush_height/2), brush.angle, 1 )
    brush_texture_rotated = cv2.warpAffine( brush_texture_scaled, transformation_matrix, (brush_width, brush_height))

    alpha = brush_texture_rotated.astype( float ) / 255.0
    alpha_3 = np.dstack( (alpha, alpha, alpha) )

    foreground = np.zeros( (*brush_texture_rotated.shape, 3), np.uint8 )
    foreground[ :, : ] = brush.color

    draw_y = int( brush.position.y - brush_width / 2 )
    draw_x = int( brush.position.x - brush_height / 2 )

    # define region of interest
    y_min = max( draw_y, 0 )
    y_max = min( draw_y + brush_height, image_height )
    x_min = max( draw_x, 0 )
    x_max = min( draw_x + brush_width, image_width )

    background_subsection = image[y_min:y_max, x_min:x_max]
    foreground_subsection = foreground[
        y_min - draw_y : y_max - draw_y,
        x_min - draw_x : x_max - draw_x
    ]
    alpha_subsection = alpha_3[
        y_min - draw_y : y_max - draw_y,
        x_min - draw_x : x_max - draw_x
    ]

    composite = background_subsection * (1 - alpha_subsection) + foreground_subsection * alpha_subsection
    image[ y_min:y_max, x_min:x_max ] = composite
    return image
