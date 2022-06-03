"""
Compositing (post processing) the rendered image.
"""

import numpy as np


def composite(libs, props, raw_img):
    """
    Convert raw image (float64) into actual image (int8).
    Also adds some effects e.g. glare.
    Will change ``raw_img``.
    """
    img = np.empty_like(raw_img, dtype=np.uint8)

    libs["composite"].composite(
        raw_img, img, img.shape[1], img.shape[0],
        props.comp.shutter,
    )

    return img
