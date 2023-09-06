import cv2
import numpy as np
import svgwrite

from genetic_algorithms.impl.pointillism import Pointillism


def bgr_to_svg_color(rgb):
    return f'rgb({int(round(rgb[2]))},{int(round(rgb[1]))},{int(round(rgb[0]))})'


def hsv_to_svg_color(hsv):
    bgr_color = cv2.cvtColor(np.uint8([[hsv]]), cv2.COLOR_HSV2BGR)[0][0]
    return bgr_to_svg_color(bgr_color)


def redraw_pointillism_as_svg(
        specimen : Pointillism.Specimen,
        use_hsv : bool,
        ellipse_scale : float,
):
    svg_image = svgwrite.Drawing( profile = 'full' )

    for ellipse in specimen.genes:
        if use_hsv:
            svg_color = hsv_to_svg_color( ellipse.color )
        else:
            svg_color = bgr_to_svg_color( ellipse.color )

        svg_position = ( ellipse.position.x, ellipse.position.y )

        svg_ellipse = svg_image.ellipse(
            center = svg_position,
            r = ( ellipse.axes[0] * ellipse_scale, ellipse.axes[1] * ellipse_scale ),
            fill = svg_color
        )
        svg_ellipse.rotate( ellipse.angle, svg_position )

        svg_image.add( svg_ellipse )

    return svg_image
