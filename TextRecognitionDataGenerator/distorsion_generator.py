import cv2
import math
import os
import random as rnd
import numpy as np

from PIL import Image, ImageDraw, ImageFilter

def _apply_func_distorsion(image, vertical, horizontal, max_offset, func):
    """
        Apply a distorsion to an image
    """

    # Nothing to do!
    if not vertical and not horizontal:
        return image

    rgb_image = image.convert('RGBA')
    
    img_arr = np.array(rgb_image)

    vertical_offsets = [func(i) for i in range(img_arr.shape[1])]
    horizontal_offsets = [
        func(i)
        for i in range(
            img_arr.shape[0] + (
                (max(vertical_offsets) - min(min(vertical_offsets), 0)) if vertical else 0
            )
        )
    ]

    new_img_arr = np.zeros((
                        img_arr.shape[0] + (2 * max_offset if vertical else 0),
                        img_arr.shape[1] + (2 * max_offset if horizontal else 0),
                        4
                    ))

    new_img_arr_copy = np.copy(new_img_arr)
    
    if vertical:
        column_height = img_arr.shape[0]
        for i, o in enumerate(vertical_offsets):
            column_pos = (i + max_offset) if horizontal else i
            new_img_arr[max_offset+o:column_height+max_offset+o, column_pos, :] = img_arr[:, i, :]

    if horizontal:
        row_width = img_arr.shape[1]
        for i, o in enumerate(horizontal_offsets):
            if vertical:
                new_img_arr_copy[i, max_offset+o:row_width+max_offset+o,:] = new_img_arr[i, max_offset:row_width+max_offset, :]
            else:
                new_img_arr[i, max_offset+o:row_width+max_offset+o,:] = img_arr[i, :, :]

    return Image.fromarray(np.uint8(new_img_arr_copy if horizontal and vertical else new_img_arr)).convert('RGBA')

def sin(image, vertical=False, horizontal=False):
    """
        Apply a sine distorsion on one or both of the specified axis
    """

    max_offset = int(image.height ** 0.5)

    return _apply_func_distorsion(image, vertical, horizontal, max_offset, (lambda x: int(math.sin(math.radians(x)) * max_offset)))

def cos(image, vertical=False, horizontal=False):
    """
        Apply a cosine distorsion on one or both of the specified axis
    """

    max_offset = int(image.height ** 0.5)

    return _apply_func_distorsion(image, vertical, horizontal, max_offset, (lambda x: int(math.cos(math.radians(x)) * max_offset)))

def random(image, vertical=False, horizontal=False):
    """
        Apply a random distorsion on one or both of the specified axis
    """

    max_offset = int(image.height ** 0.4)

    return _apply_func_distorsion(image, vertical, horizontal, max_offset, (lambda x: rnd.randint(0, max_offset)))
