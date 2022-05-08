from typing import Any

import numpy as np

from .keyframe import Keyframe, Interp


def lerp(fac, from_range, to_range) -> Any:
    """
    Linear interpolation, similar to np.interp
    Works on np.array as well.
    """
    progress = (fac-from_range[0]) / (from_range[1]-from_range[0])
    return to_range[0] + progress * (to_range[1]-to_range[0])


def quad_fac(fac):
    """
    if fac < 0.5: y = 2x^2
    else: y = -2(x-1)^2 + 1
    """
    if fac < 0.5:
        return 2 * fac**2
    else:
        return -2 * (fac-1)**2 + 1

def interpolate(k1: Keyframe, k2: Keyframe, frame: int) -> Any:
    """
    Interpolate between two keyframes.
    k1.frame <= frame < k2.frame
    """
    interp = k1.interp
    v1 = k1.value
    v2 = k2.value
    f1 = k1.frame
    f2 = k2.frame

    if interp == Interp.CONSTANT:
        return v1

    elif interp in (Interp.LINEAR, Interp.QUADRATIC):
        fac = np.interp(frame, (f1, f2), (0, 1))  # Lerp
        if interp == Interp.QUADRATIC:
            fac = quad_fac(fac)

        return lerp(fac, (0, 1), (v1, v2))
