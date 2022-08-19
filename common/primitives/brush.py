from dataclasses import dataclass
import random

import cv2
import numpy as np
from pathlib import Path

from common.primitives.color import RGBColor, random_color
from common.primitives.point import Point, random_point


@dataclass
class Brush:
    color               : RGBColor
    brush_texture_index : int
    position            : Point
    angle               : float
    scale                : float


def _preload_brush_textures():
    directory_name = Path(__file__).parent / 'watercolor_brushes/'
    texture_paths = []
    for extension in [ '.jpg', '.png' ]:
        texture_paths.extend( list( directory_name.rglob( extension ) ) )
    textures = [ cv2.imread( texture_path ) for texture_path in texture_paths ]
    textures = [ cv2.cvtColor( texture, cv2.COLOR_BGR2GRAY ) for texture in textures ]
    return textures
g_preloaded_brush_textures = _preload_brush_textures()


def random_brush_texture_index( exclude_index : int = 999 ):
    potential_texture_indices = []
    for i in range( len( g_preloaded_brush_textures ) ):
        if i is not exclude_index:
            potential_texture_indices.append( i )
    selected_texture_index = random.choice( potential_texture_indices )
    return selected_texture_index


def random_brush_size( min_size : float, max_size : float ):
    return random.uniform( min_size, max_size )


def random_brush( width, height, min_size, max_size, sampling_mask ):
    brush = Brush(
        color = random_color(),
        scale = random_brush_size( min_size, max_size ),
        position = random_point( width, height ),
    )
    return brush


def draw_brush_on_image( brush : Brush, image : np.ndarray ) -> np.ndarray:
    brush_texture = g_preloaded_brush_textures[ brush.brush_texture_index ]
    brush_height, brush_width = brush_texture.shape[:2]
    transformation_matrix = cv2.getRotationMatrix2D( (brush_width/2, brush_height/2), brush.angle, brush.scale )
    brush_texture = cv2.warpAffine( brush_texture, transformation_matrix, (brush_width, brush_height))
    brush_mask = np.zeros_like( brush_texture )
    brush_mask[(brush_texture>0)] = 1 # todo: make actual mask
    image[brush_mask] = brush_texture * brush.color
    return image