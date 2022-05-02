import numpy as np

from .keyframe import Keyframe, Interp


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

    elif interp == Interp.LINEAR:
        return np.interp(frame, (f1, f2), (v1, v2))
