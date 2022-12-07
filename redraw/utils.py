import math


def get_scale_for_4k_from_shape( current_height, current_width ):
    # using a weird definition of 4k here,
    # so that we do not change aspect ratio,
    # but get approximately the same number of pixels
    target_n_pixels = 2160 * 3840
    aspect_ratio = current_width / current_height
    new_height = math.sqrt( target_n_pixels / aspect_ratio )
    scale = new_height / current_height
    return scale


def get_scale_for_4k_from_image( image ):
    return get_scale_for_4k_from_shape( *image.shape[:2] )
