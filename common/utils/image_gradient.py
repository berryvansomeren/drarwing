import cv2
import math


def get_image_gradients_from_hsv( hsv ):
    rgb = cv2.cvtColor( hsv, cv2.COLOR_HSV2RGB )
    gray = cv2.cvtColor( rgb, cv2.COLOR_RGB2GRAY )
    dx = cv2.Scharr( gray, cv2.CV_32F, 1, 0 )
    dy = cv2.Scharr( gray, cv2.CV_32F, 0, 1 )

    s = 2 * 10 + 1
    dx = cv2.GaussianBlur( dx, (s, s), 0 )
    dy = cv2.GaussianBlur( dy, (s, s), 0 )

    return dx, dy


def get_direction_from_gradients( dx, dy, x, y ):
    direction = math.atan2(dy[y,x], dx[y,x])
    return direction


def get_magnitude_from_gradients( dx, dy, x, y ):
    magnitude = math.hypot(dx[y,x], dy[y,x])
    return magnitude