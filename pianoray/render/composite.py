"""
Compositing (post processing) the rendered image.
"""

import cv2
import numpy as np

from ..utils import bounds


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


def add_fade(props, img, frame_start, frame_end, frame):
    """
    Add intro outro fade and blur as a post processing step.

    :param img: Dtype uint8, call this function after compositing.
    """
    fps = props.video.fps
    fade_in = frame_start + props.comp.fade_in * fps
    fade_out = frame_end - props.comp.fade_out * fps

    fade_fac = 1
    if frame <= fade_in:
        fade_fac *= np.interp(frame, (frame_start, fade_in), (0, 1))
    if frame >= fade_out:
        fade_fac *= np.interp(frame, (fade_out, frame_end), (1, 0))
    fade_fac = bounds(fade_fac, 0, 1)

    if fade_fac < 1:
        blur = int(props.comp.fade_blur * (1-fade_fac))
        img[...] = (img * fade_fac).astype(np.uint8)
        if blur > 0:
            img[...] = cv2.blur(img, (blur, blur))
