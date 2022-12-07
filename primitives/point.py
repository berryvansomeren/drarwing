from dataclasses import dataclass
import random


@dataclass
class Point :
    x: int
    y: int


def random_point( width : int, height : int ) -> Point:
    random_x = int( random.random() * width )
    random_y = int( random.random() * height )
    assert 0 <= random_x < width
    assert 0 <= random_y < height
    return Point( random_x, random_y )
