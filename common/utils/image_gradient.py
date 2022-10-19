import cv2
import math

import numpy as np

from common.primitives.point import Point


class HSVImageGradient:

    def __init__( self, hsv_image : np.ndarray, blur_kernel_size = None, blur_magnitude = 0 ) :

        if blur_kernel_size is None :
            blur_kernel_size = int( min( hsv_image.shape[ :2 ] ) / 50 )
        if blur_kernel_size % 2 == 0 :
            blur_kernel_size += 1

        rgb = cv2.cvtColor( hsv_image, cv2.COLOR_HSV2RGB )
        gray = cv2.cvtColor( rgb, cv2.COLOR_RGB2GRAY )
        dx = cv2.Scharr( gray, cv2.CV_32F, 1, 0 )
        dy = cv2.Scharr( gray, cv2.CV_32F, 0, 1 )

        blur_kernel_size_2d = (blur_kernel_size, blur_kernel_size)
        self._dx = cv2.GaussianBlur( dx, blur_kernel_size_2d, blur_magnitude )
        self._dy = cv2.GaussianBlur( dy, blur_kernel_size_2d, blur_magnitude )


    def get_direction( self, position : Point ):
        dy = self._dy[position.y,position.x]
        dx = self._dx[position.y,position.x]
        direction = math.degrees( math.atan2( dy, dx ) )
        return direction


    def get_magnitude( self, position : Point ):
        dy = self._dy[position.y,position.x]
        dx = self._dx[position.y,position.x]
        magnitude = math.hypot( dy, dx )
        return magnitude
