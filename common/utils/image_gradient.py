import cv2
import math


def get_image_gradients_from_hsv( hsv, blur_kernel_size = None, blur_magnitude = 0 ):

    if blur_kernel_size is None:
        blur_kernel_size = int( min( hsv.shape[ :2 ] ) / 50 )
    if blur_kernel_size % 2 == 0 :
        blur_kernel_size += 1

    rgb = cv2.cvtColor( hsv, cv2.COLOR_HSV2RGB )
    gray = cv2.cvtColor( rgb, cv2.COLOR_RGB2GRAY )
    dx = cv2.Scharr( gray, cv2.CV_32F, 1, 0 )
    dy = cv2.Scharr( gray, cv2.CV_32F, 0, 1 )

    blur_kernel_size_2d = ( blur_kernel_size, blur_kernel_size )
    dx = cv2.GaussianBlur( dx, blur_kernel_size_2d, blur_magnitude )
    dy = cv2.GaussianBlur( dy, blur_kernel_size_2d, blur_magnitude )

    return dx, dy


def get_direction_from_gradients( dx, dy, x, y ):
    direction = math.atan2(dy[y,x], dx[y,x])
    return direction


def get_magnitude_from_gradients( dx, dy, x, y ):
    magnitude = math.hypot(dx[y,x], dy[y,x])
    return magnitude