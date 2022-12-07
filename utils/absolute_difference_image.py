import cv2
import numpy as np


def get_absolute_difference_image( specimen_image, target_image ) -> np.ndarray:
    diff_image_3 = cv2.absdiff(
        np.array( specimen_image, np.int16 ),
        np.array( target_image, np.int16 )
    )
    diff_image_1 = np.sum(diff_image_3, axis=2) / 3 # divide by 3 because we summed 3 channels
    return diff_image_1
